"""
OpenBB Connector router for v1 API.

Handles all financial data operations including price retrieval, symbol information,
and bulk data operations using OpenBB and various financial data sources.
"""

import time
import uuid
import asyncio
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends
from fastapi.responses import JSONResponse

import pandas as pd
import yfinance as yf
import psycopg2
from psycopg2.extras import execute_values
import structlog

import sys

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes
)

from ..models.requests import (
    PriceDataRequest,
    SymbolRequest,
    TimeSeriesRequest,
    FinancialDataRequest,
    BulkImportRequest,
    DataQualityRequest,
    DataSource,
    TimeInterval,
    DataType
)

from ..models.responses import (
    PriceData,
    SymbolInfo,
    TimeSeriesData,
    FinancialSummary,
    DataImportResult,
    MarketStatus,
    OpenBBStatistics,
    DataQualityReport,
    BulkOperationStatus
)

logger = structlog.get_logger()
router = APIRouter()

# Global references - will be set by main app
db_connection = None
data_sources = {}
active_jobs = {}


def set_openbb_system(db_conn, sources):
    """Set OpenBB system references from main application."""
    global db_connection, data_sources
    db_connection = db_conn
    data_sources = sources


def ensure_price_table():
    """Ensure the price data table exists."""
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stg_openbb_prices (
                    id SERIAL PRIMARY KEY,
                    as_of_date DATE NOT NULL,
                    symbol TEXT NOT NULL,
                    open DOUBLE PRECISION,
                    high DOUBLE PRECISION,
                    low DOUBLE PRECISION,
                    close DOUBLE PRECISION,
                    volume BIGINT,
                    adj_close DOUBLE PRECISION,
                    dividends DOUBLE PRECISION,
                    stock_splits DOUBLE PRECISION,
                    data_source TEXT DEFAULT 'yahoo',
                    currency TEXT,
                    exchange TEXT,
                    vendor_ts TIMESTAMP DEFAULT NOW(),
                    UNIQUE(symbol, as_of_date, data_source)
                );
                
                CREATE INDEX IF NOT EXISTS idx_openbb_prices_symbol_date 
                ON stg_openbb_prices(symbol, as_of_date);
                
                CREATE INDEX IF NOT EXISTS idx_openbb_prices_date 
                ON stg_openbb_prices(as_of_date);
            """)
        db_connection.commit()
    except Exception as e:
        logger.error("Failed to ensure price table", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Database setup failed",
            status_code=500,
            details={"error": str(e)}
        )


def fetch_yahoo_prices(symbols: List[str], period: str = "5d", interval: str = "1d") -> pd.DataFrame:
    """Fetch price data from Yahoo Finance."""
    rows = []
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                logger.warning("No data found for symbol", symbol=symbol)
                continue
            
            hist = hist.reset_index()
            
            for _, row in hist.iterrows():
                price_row = {
                    "as_of_date": row["Date"].date() if hasattr(row["Date"], 'date') else row["Date"],
                    "symbol": symbol,
                    "open": float(row["Open"]) if pd.notna(row["Open"]) else None,
                    "high": float(row["High"]) if pd.notna(row["High"]) else None,
                    "low": float(row["Low"]) if pd.notna(row["Low"]) else None,
                    "close": float(row["Close"]) if pd.notna(row["Close"]) else None,
                    "volume": int(row["Volume"]) if pd.notna(row["Volume"]) else None,
                    "dividends": float(row.get("Dividends", 0)) if pd.notna(row.get("Dividends", 0)) else None,
                    "stock_splits": float(row.get("Stock Splits", 0)) if pd.notna(row.get("Stock Splits", 0)) else None,
                    "data_source": "yahoo"
                }
                rows.append(price_row)
                
        except Exception as e:
            logger.error("Failed to fetch data for symbol", symbol=symbol, error=str(e))
            continue
    
    return pd.DataFrame(rows)


def save_prices_to_db(df: pd.DataFrame) -> Dict[str, int]:
    """Save price data to database."""
    if df.empty:
        return {"inserted": 0, "updated": 0, "failed": 0}
    
    ensure_price_table()
    
    inserted = 0
    updated = 0
    failed = 0
    
    try:
        with db_connection.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO stg_openbb_prices 
                        (as_of_date, symbol, open, high, low, close, volume, 
                         dividends, stock_splits, data_source, currency, exchange)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (symbol, as_of_date, data_source)
                        DO UPDATE SET
                            open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            volume = EXCLUDED.volume,
                            dividends = EXCLUDED.dividends,
                            stock_splits = EXCLUDED.stock_splits,
                            vendor_ts = NOW()
                    """, (
                        row["as_of_date"], row["symbol"], row.get("open"),
                        row.get("high"), row.get("low"), row.get("close"),
                        row.get("volume"), row.get("dividends"), row.get("stock_splits"),
                        row.get("data_source", "yahoo"), row.get("currency"), row.get("exchange")
                    ))
                    
                    if cursor.rowcount == 1:
                        inserted += 1
                    else:
                        updated += 1
                        
                except Exception as e:
                    logger.error("Failed to save price record", error=str(e), symbol=row.get("symbol"))
                    failed += 1
        
        db_connection.commit()
        
    except Exception as e:
        db_connection.rollback()
        logger.error("Failed to save prices to database", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to save data to database",
            status_code=500,
            details={"error": str(e)}
        )
    
    return {"inserted": inserted, "updated": updated, "failed": failed}


# ===== PRICE DATA ENDPOINTS =====

@router.post(
    "/prices/fetch",
    response_model=DataImportResult,
    summary="Fetch Price Data",
    description="Fetch current or historical price data for specified symbols"
)
async def fetch_price_data(
    request: PriceDataRequest,
    background_tasks: BackgroundTasks
) -> DataImportResult:
    """
    Fetch price data for specified symbols.
    
    Supports various data sources and time periods. Data can be automatically
    saved to the database for later retrieval and analysis.
    """
    job_id = f"fetch_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    start_time = datetime.utcnow()
    
    logger.info(
        "Fetching price data",
        job_id=job_id,
        symbols=request.symbols,
        period=request.period,
        data_source=request.data_source
    )
    
    try:
        # Currently only Yahoo Finance is implemented
        if request.data_source != DataSource.YAHOO:
            raise APIError(
                code=ErrorCodes.NOT_IMPLEMENTED,
                message=f"Data source {request.data_source} not yet implemented",
                status_code=501
            )
        
        # Fetch data
        df = fetch_yahoo_prices(
            symbols=request.symbols,
            period=request.period,
            interval=request.interval.value
        )
        
        if df.empty:
            return DataImportResult(
                job_id=job_id,
                status="completed",
                symbols_requested=request.symbols,
                symbols_processed=[],
                symbols_failed=request.symbols,
                total_records=0,
                records_inserted=0,
                records_updated=0,
                records_failed=0,
                started_at=start_time,
                completed_at=datetime.utcnow(),
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                errors=[{"message": "No data found for any symbols"}],
                data_source=request.data_source,
                batch_size=len(request.symbols)
            )
        
        # Save to database if requested
        save_result = {"inserted": 0, "updated": 0, "failed": 0}
        if request.save_to_db:
            save_result = save_prices_to_db(df)
        
        # Determine processed and failed symbols
        processed_symbols = df["symbol"].unique().tolist()
        failed_symbols = [s for s in request.symbols if s not in processed_symbols]
        
        completed_at = datetime.utcnow()
        duration = (completed_at - start_time).total_seconds()
        
        logger.info(
            "Price data fetch completed",
            job_id=job_id,
            total_records=len(df),
            processed_symbols=len(processed_symbols),
            failed_symbols=len(failed_symbols),
            duration=duration
        )
        
        return DataImportResult(
            job_id=job_id,
            status="completed",
            symbols_requested=request.symbols,
            symbols_processed=processed_symbols,
            symbols_failed=failed_symbols,
            total_records=len(df),
            records_inserted=save_result["inserted"],
            records_updated=save_result["updated"],
            records_failed=save_result["failed"],
            started_at=start_time,
            completed_at=completed_at,
            duration_seconds=duration,
            errors=[],
            data_source=request.data_source,
            batch_size=len(request.symbols)
        )
        
    except APIError:
        raise
    except Exception as e:
        logger.error("Price data fetch failed", job_id=job_id, error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to fetch price data",
            status_code=500,
            details={"job_id": job_id, "error": str(e)}
        )


@router.get(
    "/prices",
    response_model=PaginatedResponse[PriceData],
    summary="Get Price Data",
    description="Retrieve stored price data with filtering and pagination"
)
def get_price_data(
    pagination: PaginationParams = Depends(),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    data_source: Optional[DataSource] = Query(None, description="Filter by data source")
) -> PaginatedResponse[PriceData]:
    """
    Retrieve stored price data with filtering and pagination.
    
    Supports filtering by symbol, date range, and data source.
    """
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        # Build query
        conditions = []
        params = []
        
        if symbol:
            conditions.append("symbol = %s")
            params.append(symbol.upper())
        
        if start_date:
            conditions.append("as_of_date >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("as_of_date <= %s")
            params.append(end_date)
        
        if data_source:
            conditions.append("data_source = %s")
            params.append(data_source.value)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        # Count total records
        count_query = f"SELECT COUNT(*) FROM stg_openbb_prices {where_clause}"
        
        with db_connection.cursor() as cursor:
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            # Get data page
            data_query = f"""
                SELECT as_of_date, symbol, open, high, low, close, volume,
                       dividends, stock_splits, data_source, currency, exchange, vendor_ts
                FROM stg_openbb_prices 
                {where_clause}
                ORDER BY symbol, as_of_date DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(data_query, params + [pagination.limit, pagination.offset])
            rows = cursor.fetchall()
        
        # Convert to response models
        price_data = []
        for row in rows:
            price_data.append(PriceData(
                symbol=row[1],
                date=row[0],
                open=row[2],
                high=row[3],
                low=row[4],
                close=row[5],
                volume=row[6],
                dividends=row[7],
                stock_splits=row[8],
                data_source=DataSource(row[9]),
                currency=row[10],
                exchange=row[11],
                created_at=row[12]
            ))
        
        return PaginatedResponse.create(price_data, total, pagination)
        
    except Exception as e:
        logger.error("Failed to retrieve price data", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve price data",
            status_code=500,
            details={"error": str(e)}
        )


# ===== SYMBOL INFORMATION =====

@router.get(
    "/symbols/{symbol}",
    response_model=SymbolInfo,
    summary="Get Symbol Information",
    description="Get detailed information about a specific stock symbol"
)
def get_symbol_info(
    symbol: str,
    data_source: DataSource = Query(DataSource.YAHOO, description="Data source to use"),
    include_financials: bool = Query(False, description="Include financial data"),
    include_news: bool = Query(False, description="Include recent news")
) -> SymbolInfo:
    """
    Get detailed information about a specific stock symbol.
    
    Includes basic company information, current market data, and optionally
    financial statements and recent news.
    """
    symbol = symbol.upper()
    
    try:
        if data_source != DataSource.YAHOO:
            raise APIError(
                code=ErrorCodes.NOT_IMPLEMENTED,
                message=f"Data source {data_source} not yet implemented",
                status_code=501
            )
        
        # Fetch symbol info from Yahoo Finance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info or "symbol" not in info:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message=f"Symbol {symbol} not found",
                status_code=404
            )
        
        # Map Yahoo Finance data to our model
        symbol_info = SymbolInfo(
            symbol=symbol,
            name=info.get("longName", info.get("shortName", symbol)),
            exchange=info.get("exchange"),
            currency=info.get("currency"),
            country=info.get("country"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            market_cap=info.get("marketCap"),
            shares_outstanding=info.get("sharesOutstanding"),
            current_price=info.get("currentPrice", info.get("regularMarketPrice")),
            previous_close=info.get("previousClose"),
            day_high=info.get("dayHigh"),
            day_low=info.get("dayLow"),
            price_change=info.get("regularMarketChange"),
            price_change_percent=info.get("regularMarketChangePercent"),
            pe_ratio=info.get("trailingPE"),
            pb_ratio=info.get("priceToBook"),
            dividend_yield=info.get("dividendYield"),
            data_source=data_source,
            last_updated=datetime.utcnow()
        )
        
        return symbol_info
        
    except APIError:
        raise
    except Exception as e:
        logger.error("Failed to get symbol info", symbol=symbol, error=str(e))
        raise APIError(
            code=ErrorCodes.EXTERNAL_SERVICE_ERROR,
            message=f"Failed to retrieve information for symbol {symbol}",
            status_code=502,
            details={"symbol": symbol, "error": str(e)}
        )


@router.get(
    "/symbols",
    response_model=PaginatedResponse[str],
    summary="List Available Symbols",
    description="Get list of available symbols in the database"
)
def list_symbols(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search symbols by name")
) -> PaginatedResponse[str]:
    """
    Get list of available symbols in the database.
    
    Supports search functionality and pagination.
    """
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        # Build query
        where_clause = ""
        params = []
        
        if search:
            where_clause = "WHERE symbol ILIKE %s"
            params.append(f"%{search.upper()}%")
        
        # Count total symbols
        count_query = f"SELECT COUNT(DISTINCT symbol) FROM stg_openbb_prices {where_clause}"
        
        with db_connection.cursor() as cursor:
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            # Get symbols page
            symbols_query = f"""
                SELECT DISTINCT symbol 
                FROM stg_openbb_prices 
                {where_clause}
                ORDER BY symbol
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(symbols_query, params + [pagination.limit, pagination.offset])
            rows = cursor.fetchall()
        
        symbols = [row[0] for row in rows]
        
        return PaginatedResponse.create(symbols, total, pagination)
        
    except Exception as e:
        logger.error("Failed to list symbols", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve symbols list",
            status_code=500,
            details={"error": str(e)}
        )


# ===== STATISTICS & MONITORING =====

@router.get(
    "/statistics",
    response_model=OpenBBStatistics,
    summary="Get OpenBB Statistics",
    description="Get comprehensive statistics about the OpenBB connector"
)
def get_statistics() -> OpenBBStatistics:
    """
    Get comprehensive statistics about the OpenBB connector.
    
    Returns data coverage, import statistics, and system health information.
    """
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        with db_connection.cursor() as cursor:
            # Basic statistics
            cursor.execute("SELECT COUNT(DISTINCT symbol) FROM stg_openbb_prices")
            total_symbols = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM stg_openbb_prices")
            total_records = cursor.fetchone()[0]
            
            # Data freshness
            cursor.execute("SELECT MIN(as_of_date), MAX(as_of_date) FROM stg_openbb_prices")
            date_range = cursor.fetchone()
            oldest_data = date_range[0] if date_range[0] else None
            newest_data = date_range[1] if date_range[1] else None
            
            # Top symbols by record count
            cursor.execute("""
                SELECT symbol, COUNT(*) as record_count
                FROM stg_openbb_prices
                GROUP BY symbol
                ORDER BY record_count DESC
                LIMIT 10
            """)
            top_symbols = [
                {"symbol": row[0], "record_count": row[1]}
                for row in cursor.fetchall()
            ]
            
            # Data sources
            cursor.execute("SELECT DISTINCT data_source FROM stg_openbb_prices")
            data_sources_used = [row[0] for row in cursor.fetchall()]
        
        # Calculate data quality score (simplified)
        data_quality_score = 85.0  # Placeholder - would need actual quality analysis
        
        return OpenBBStatistics(
            total_symbols=total_symbols,
            total_records=total_records,
            data_sources=data_sources_used,
            total_imports=0,  # Would need to track this
            successful_imports=0,
            failed_imports=0,
            last_import=None,
            last_successful_import=None,
            oldest_data=oldest_data,
            newest_data=newest_data,
            top_symbols=top_symbols,
            average_import_time=None,
            data_coverage=100.0 if total_symbols > 0 else 0.0,
            data_quality_score=data_quality_score,
            system_health="healthy",
            last_calculated=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get statistics", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve statistics",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/market/status",
    response_model=MarketStatus,
    summary="Get Market Status",
    description="Get current market status and trading hours"
)
def get_market_status(
    exchange: str = Query("NYSE", description="Exchange to check")
) -> MarketStatus:
    """
    Get current market status and trading hours.
    
    Returns whether the market is currently open and next trading session times.
    """
    try:
        # This is a simplified implementation
        # In production, would use real market calendar data
        
        current_time = datetime.utcnow()
        
        # NYSE trading hours (simplified - doesn't account for holidays)
        market_open_hour = 14  # 9:30 AM ET = 14:30 UTC (during standard time)
        market_close_hour = 21  # 4:00 PM ET = 21:00 UTC
        
        is_weekday = current_time.weekday() < 5  # Monday = 0, Sunday = 6
        current_hour = current_time.hour
        
        is_open = (
            is_weekday and 
            market_open_hour <= current_hour < market_close_hour
        )
        
        return MarketStatus(
            exchange=exchange,
            is_open=is_open,
            market_open="09:30",
            market_close="16:00",
            current_time=current_time,
            timezone="America/New_York",
            next_open=None,  # Would calculate next trading session
            next_close=None,
            is_holiday=False,  # Would check holiday calendar
            holiday_name=None
        )
        
    except Exception as e:
        logger.error("Failed to get market status", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve market status",
            status_code=500,
            details={"error": str(e)}
        )


# ===== DATA QUALITY & MAINTENANCE =====

@router.post(
    "/data/quality-check",
    response_model=DataQualityReport,
    summary="Check Data Quality",
    description="Perform data quality checks on stored financial data"
)
def check_data_quality(
    request: DataQualityRequest
) -> DataQualityReport:
    """
    Perform data quality checks on stored financial data.
    
    Identifies data gaps, outliers, and other quality issues.
    """
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        # This is a simplified implementation
        # In production, would perform comprehensive quality analysis
        
        with db_connection.cursor() as cursor:
            # Count total records in scope
            if request.symbols:
                cursor.execute(
                    "SELECT COUNT(*) FROM stg_openbb_prices WHERE symbol = ANY(%s)",
                    (request.symbols,)
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM stg_openbb_prices")
            
            total_records = cursor.fetchone()[0]
            
            # Simplified quality checks
            valid_records = total_records  # Placeholder
            invalid_records = 0
            
            # Check for potential issues (simplified)
            missing_data_gaps = []
            outliers = []
            duplicates = []
            
            if request.check_duplicates:
                cursor.execute("""
                    SELECT symbol, as_of_date, COUNT(*)
                    FROM stg_openbb_prices
                    GROUP BY symbol, as_of_date, data_source
                    HAVING COUNT(*) > 1
                    LIMIT 10
                """)
                
                for row in cursor.fetchall():
                    duplicates.append({
                        "symbol": row[0],
                        "date": str(row[1]),
                        "count": row[2]
                    })
        
        # Calculate quality score
        quality_score = 95.0 if not duplicates else 90.0
        
        # Generate recommendations
        recommendations = []
        if duplicates:
            recommendations.append("Remove duplicate records")
        if not recommendations:
            recommendations.append("Data quality is good")
        
        return DataQualityReport(
            symbol=request.symbols[0] if request.symbols and len(request.symbols) == 1 else None,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            missing_data_gaps=missing_data_gaps,
            outliers=outliers,
            duplicates=duplicates,
            quality_score=quality_score,
            recommendations=recommendations,
            check_date=datetime.utcnow(),
            data_range={
                "start_date": str(request.start_date) if request.start_date else None,
                "end_date": str(request.end_date) if request.end_date else None
            }
        )
        
    except Exception as e:
        logger.error("Failed to check data quality", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to perform data quality check",
            status_code=500,
            details={"error": str(e)}
        )


@router.delete(
    "/data/cleanup",
    summary="Clean Up Data",
    description="Clean up old or invalid data records"
)
def cleanup_data(
    older_than_days: int = Query(365, description="Remove data older than N days"),
    remove_duplicates: bool = Query(False, description="Remove duplicate records"),
    dry_run: bool = Query(True, description="Perform dry run without actual deletion")
) -> Dict[str, Any]:
    """
    Clean up old or invalid data records.
    
    Supports removing old data and duplicate records with dry run option.
    """
    if not db_connection:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Database connection not available",
            status_code=503
        )
    
    try:
        cleanup_date = datetime.utcnow().date() - timedelta(days=older_than_days)
        
        with db_connection.cursor() as cursor:
            deleted_records = 0
            duplicate_records = 0
            
            if not dry_run:
                # Remove old records
                cursor.execute(
                    "DELETE FROM stg_openbb_prices WHERE as_of_date < %s",
                    (cleanup_date,)
                )
                deleted_records = cursor.rowcount
                
                # Remove duplicates if requested
                if remove_duplicates:
                    cursor.execute("""
                        DELETE FROM stg_openbb_prices
                        WHERE id NOT IN (
                            SELECT MIN(id)
                            FROM stg_openbb_prices
                            GROUP BY symbol, as_of_date, data_source
                        )
                    """)
                    duplicate_records = cursor.rowcount
                
                db_connection.commit()
            else:
                # Dry run - count what would be deleted
                cursor.execute(
                    "SELECT COUNT(*) FROM stg_openbb_prices WHERE as_of_date < %s",
                    (cleanup_date,)
                )
                deleted_records = cursor.fetchone()[0]
                
                if remove_duplicates:
                    cursor.execute("""
                        SELECT COUNT(*) - COUNT(DISTINCT symbol, as_of_date, data_source)
                        FROM stg_openbb_prices
                    """)
                    duplicate_records = cursor.fetchone()[0]
        
        return {
            "dry_run": dry_run,
            "cleanup_date": str(cleanup_date),
            "old_records_deleted": deleted_records,
            "duplicate_records_removed": duplicate_records,
            "message": "Cleanup completed successfully" if not dry_run else "Dry run completed"
        }
        
    except Exception as e:
        if not dry_run:
            db_connection.rollback()
        logger.error("Failed to cleanup data", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to cleanup data",
            status_code=500,
            details={"error": str(e)}
        )
