"""
Response models for OpenBB Connector API.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from .requests import DataSource, TimeInterval, DataType


class PriceData(BaseModel):
    """Price data for a stock symbol."""
    
    symbol: str = Field(..., description="Stock symbol")
    date: date = Field(..., description="Date of the price data")
    
    open: Optional[float] = Field(None, description="Opening price")
    high: Optional[float] = Field(None, description="High price")
    low: Optional[float] = Field(None, description="Low price")
    close: Optional[float] = Field(None, description="Closing price")
    volume: Optional[int] = Field(None, description="Trading volume")
    
    adj_close: Optional[float] = Field(None, description="Adjusted closing price")
    
    # Additional fields
    dividends: Optional[float] = Field(None, description="Dividend amount")
    stock_splits: Optional[float] = Field(None, description="Stock split ratio")
    
    # Metadata
    data_source: DataSource = Field(..., description="Source of the data")
    currency: Optional[str] = Field(None, description="Currency")
    exchange: Optional[str] = Field(None, description="Exchange")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation time")


class SymbolInfo(BaseModel):
    """Information about a stock symbol."""
    
    symbol: str = Field(..., description="Stock symbol")
    name: str = Field(..., description="Company name")
    
    # Basic info
    exchange: Optional[str] = Field(None, description="Exchange")
    currency: Optional[str] = Field(None, description="Currency")
    country: Optional[str] = Field(None, description="Country")
    sector: Optional[str] = Field(None, description="Sector")
    industry: Optional[str] = Field(None, description="Industry")
    
    # Market data
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    shares_outstanding: Optional[int] = Field(None, description="Shares outstanding")
    
    # Price info
    current_price: Optional[float] = Field(None, description="Current price")
    previous_close: Optional[float] = Field(None, description="Previous close")
    day_high: Optional[float] = Field(None, description="Day high")
    day_low: Optional[float] = Field(None, description="Day low")
    
    # Performance
    price_change: Optional[float] = Field(None, description="Price change")
    price_change_percent: Optional[float] = Field(None, description="Price change percentage")
    
    # Ratios
    pe_ratio: Optional[float] = Field(None, description="P/E ratio")
    pb_ratio: Optional[float] = Field(None, description="P/B ratio")
    dividend_yield: Optional[float] = Field(None, description="Dividend yield")
    
    # Metadata
    data_source: DataSource = Field(..., description="Source of the data")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")


class TimeSeriesData(BaseModel):
    """Time series data for a symbol."""
    
    symbol: str = Field(..., description="Stock symbol")
    data_type: DataType = Field(..., description="Type of data")
    interval: TimeInterval = Field(..., description="Data interval")
    
    data_points: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Time series data points"
    )
    
    start_date: Optional[date] = Field(None, description="Start date of data")
    end_date: Optional[date] = Field(None, description="End date of data")
    
    count: int = Field(default=0, description="Number of data points")
    
    # Statistics
    min_value: Optional[float] = Field(None, description="Minimum value")
    max_value: Optional[float] = Field(None, description="Maximum value")
    avg_value: Optional[float] = Field(None, description="Average value")
    
    data_source: DataSource = Field(..., description="Source of the data")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")


class FinancialSummary(BaseModel):
    """Financial summary for a symbol."""
    
    symbol: str = Field(..., description="Stock symbol")
    name: str = Field(..., description="Company name")
    
    # Financial metrics
    revenue: Optional[float] = Field(None, description="Total revenue")
    net_income: Optional[float] = Field(None, description="Net income")
    total_assets: Optional[float] = Field(None, description="Total assets")
    total_debt: Optional[float] = Field(None, description="Total debt")
    cash: Optional[float] = Field(None, description="Cash and equivalents")
    
    # Ratios
    gross_margin: Optional[float] = Field(None, description="Gross margin")
    operating_margin: Optional[float] = Field(None, description="Operating margin")
    net_margin: Optional[float] = Field(None, description="Net margin")
    roe: Optional[float] = Field(None, description="Return on equity")
    roa: Optional[float] = Field(None, description="Return on assets")
    
    # Growth metrics
    revenue_growth: Optional[float] = Field(None, description="Revenue growth")
    earnings_growth: Optional[float] = Field(None, description="Earnings growth")
    
    # Valuation
    pe_ratio: Optional[float] = Field(None, description="P/E ratio")
    pb_ratio: Optional[float] = Field(None, description="P/B ratio")
    ev_ebitda: Optional[float] = Field(None, description="EV/EBITDA")
    
    # Period info
    fiscal_year: Optional[int] = Field(None, description="Fiscal year")
    quarter: Optional[str] = Field(None, description="Quarter")
    
    data_source: DataSource = Field(..., description="Source of the data")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")


class DataImportResult(BaseModel):
    """Result of data import operation."""
    
    job_id: str = Field(..., description="Import job ID")
    status: str = Field(..., description="Import status")
    
    # Import details
    symbols_requested: List[str] = Field(default_factory=list, description="Symbols requested")
    symbols_processed: List[str] = Field(default_factory=list, description="Symbols processed")
    symbols_failed: List[str] = Field(default_factory=list, description="Symbols that failed")
    
    # Statistics
    total_records: int = Field(default=0, description="Total records imported")
    records_inserted: int = Field(default=0, description="Records inserted")
    records_updated: int = Field(default=0, description="Records updated")
    records_failed: int = Field(default=0, description="Records failed")
    
    # Timing
    started_at: datetime = Field(..., description="Import start time")
    completed_at: Optional[datetime] = Field(None, description="Import completion time")
    duration_seconds: Optional[float] = Field(None, description="Import duration")
    
    # Errors
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Import errors"
    )
    
    # Metadata
    data_source: DataSource = Field(..., description="Data source used")
    batch_size: int = Field(..., description="Batch size used")


class MarketStatus(BaseModel):
    """Market status information."""
    
    exchange: str = Field(..., description="Exchange name")
    is_open: bool = Field(..., description="Whether market is open")
    
    # Market hours
    market_open: Optional[str] = Field(None, description="Market open time")
    market_close: Optional[str] = Field(None, description="Market close time")
    
    # Current status
    current_time: datetime = Field(default_factory=datetime.utcnow, description="Current time")
    timezone: str = Field(..., description="Market timezone")
    
    # Next market session
    next_open: Optional[datetime] = Field(None, description="Next market open")
    next_close: Optional[datetime] = Field(None, description="Next market close")
    
    # Holiday info
    is_holiday: bool = Field(default=False, description="Whether today is a holiday")
    holiday_name: Optional[str] = Field(None, description="Holiday name if applicable")


class OpenBBStatistics(BaseModel):
    """OpenBB connector statistics."""
    
    # Data statistics
    total_symbols: int = Field(default=0, description="Total symbols in database")
    total_records: int = Field(default=0, description="Total price records")
    data_sources: List[str] = Field(default_factory=list, description="Available data sources")
    
    # Import statistics
    total_imports: int = Field(default=0, description="Total imports performed")
    successful_imports: int = Field(default=0, description="Successful imports")
    failed_imports: int = Field(default=0, description="Failed imports")
    
    # Recent activity
    last_import: Optional[datetime] = Field(None, description="Last import time")
    last_successful_import: Optional[datetime] = Field(None, description="Last successful import")
    
    # Data freshness
    oldest_data: Optional[date] = Field(None, description="Oldest data date")
    newest_data: Optional[date] = Field(None, description="Newest data date")
    
    # Popular symbols
    top_symbols: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most frequently updated symbols"
    )
    
    # Performance metrics
    average_import_time: Optional[float] = Field(None, description="Average import time in seconds")
    data_coverage: Optional[float] = Field(None, description="Data coverage percentage")
    
    # Health indicators
    data_quality_score: Optional[float] = Field(None, description="Overall data quality score")
    system_health: str = Field(default="unknown", description="System health status")
    
    last_calculated: datetime = Field(default_factory=datetime.utcnow, description="Last calculation time")


class DataQualityReport(BaseModel):
    """Data quality report."""
    
    symbol: Optional[str] = Field(None, description="Symbol (if specific symbol check)")
    
    # Quality metrics
    total_records: int = Field(default=0, description="Total records checked")
    valid_records: int = Field(default=0, description="Valid records")
    invalid_records: int = Field(default=0, description="Invalid records")
    
    # Specific issues
    missing_data_gaps: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Identified data gaps"
    )
    
    outliers: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Identified outliers"
    )
    
    duplicates: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Duplicate records"
    )
    
    # Quality score
    quality_score: float = Field(default=0.0, description="Overall quality score (0-100)")
    
    # Recommendations
    recommendations: List[str] = Field(
        default_factory=list,
        description="Data quality improvement recommendations"
    )
    
    # Metadata
    check_date: datetime = Field(default_factory=datetime.utcnow, description="Check date")
    data_range: Dict[str, Any] = Field(
        default_factory=dict,
        description="Date range checked"
    )


class BulkOperationStatus(BaseModel):
    """Status of bulk operation."""
    
    operation_id: str = Field(..., description="Operation ID")
    operation_type: str = Field(..., description="Type of operation")
    status: str = Field(..., description="Current status")
    
    # Progress
    total_items: int = Field(..., description="Total items to process")
    completed_items: int = Field(default=0, description="Completed items")
    failed_items: int = Field(default=0, description="Failed items")
    progress_percentage: float = Field(default=0.0, description="Progress percentage")
    
    # Timing
    started_at: datetime = Field(..., description="Operation start time")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    
    # Current processing
    current_item: Optional[str] = Field(None, description="Currently processing item")
    current_batch: Optional[int] = Field(None, description="Current batch number")
    
    # Results
    results: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Operation results"
    )
    
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Operation errors"
    )
