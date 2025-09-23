"""
Request models for OpenBB Connector API.
"""

from typing import List, Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class DataSource(str, Enum):
    """Available data sources for financial data."""
    YAHOO = "yahoo"
    ALPHA_VANTAGE = "alpha_vantage"
    QUANDL = "quandl"
    FRED = "fred"
    IEX = "iex"
    POLYGON = "polygon"


class TimeInterval(str, Enum):
    """Time intervals for financial data."""
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    WEEK_1 = "1wk"
    MONTH_1 = "1mo"


class DataType(str, Enum):
    """Types of financial data."""
    PRICES = "prices"
    DIVIDENDS = "dividends"
    SPLITS = "splits"
    FINANCIALS = "financials"
    EARNINGS = "earnings"
    OPTIONS = "options"
    NEWS = "news"


class PriceDataRequest(BaseModel):
    """Request model for price data retrieval."""
    
    symbols: List[str] = Field(
        ...,
        description="List of stock symbols to fetch",
        min_items=1,
        max_items=50
    )
    
    start_date: Optional[date] = Field(
        default=None,
        description="Start date for data retrieval"
    )
    
    end_date: Optional[date] = Field(
        default=None,
        description="End date for data retrieval"
    )
    
    period: str = Field(
        default="5d",
        description="Period for data retrieval (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
    )
    
    interval: TimeInterval = Field(
        default=TimeInterval.DAY_1,
        description="Data interval"
    )
    
    data_source: DataSource = Field(
        default=DataSource.YAHOO,
        description="Data source to use"
    )
    
    include_prepost: bool = Field(
        default=False,
        description="Include pre-market and post-market data"
    )
    
    auto_adjust: bool = Field(
        default=True,
        description="Automatically adjust prices for splits and dividends"
    )
    
    save_to_db: bool = Field(
        default=True,
        description="Save retrieved data to database"
    )
    
    @validator('symbols')
    def validate_symbols(cls, v):
        """Validate stock symbols format."""
        for symbol in v:
            if not symbol or len(symbol) > 10:
                raise ValueError(f"Invalid symbol: {symbol}")
            # Basic symbol validation
            if not symbol.replace('.', '').replace('-', '').isalnum():
                raise ValueError(f"Symbol contains invalid characters: {symbol}")
        return [s.upper() for s in v]
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Validate date range is logical."""
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError("End date cannot be before start date")
        return v


class SymbolRequest(BaseModel):
    """Request model for symbol information."""
    
    symbol: str = Field(
        ...,
        description="Stock symbol to lookup",
        max_length=10
    )
    
    data_source: DataSource = Field(
        default=DataSource.YAHOO,
        description="Data source to use"
    )
    
    include_financials: bool = Field(
        default=False,
        description="Include financial statements"
    )
    
    include_news: bool = Field(
        default=False,
        description="Include recent news"
    )
    
    @validator('symbol')
    def validate_symbol(cls, v):
        """Validate symbol format."""
        if not v or len(v) > 10:
            raise ValueError("Invalid symbol length")
        return v.upper()


class TimeSeriesRequest(BaseModel):
    """Request model for time series data."""
    
    symbol: str = Field(
        ...,
        description="Stock symbol",
        max_length=10
    )
    
    data_type: DataType = Field(
        default=DataType.PRICES,
        description="Type of time series data"
    )
    
    period: str = Field(
        default="1y",
        description="Time period for data"
    )
    
    interval: TimeInterval = Field(
        default=TimeInterval.DAY_1,
        description="Data interval"
    )
    
    data_source: DataSource = Field(
        default=DataSource.YAHOO,
        description="Data source to use"
    )


class FinancialDataRequest(BaseModel):
    """Request model for financial data analysis."""
    
    symbols: List[str] = Field(
        ...,
        description="List of symbols to analyze",
        min_items=1,
        max_items=20
    )
    
    include_ratios: bool = Field(
        default=True,
        description="Include financial ratios"
    )
    
    include_growth: bool = Field(
        default=True,
        description="Include growth metrics"
    )
    
    include_valuation: bool = Field(
        default=True,
        description="Include valuation metrics"
    )
    
    quarters: int = Field(
        default=4,
        description="Number of quarters to analyze",
        ge=1,
        le=20
    )
    
    data_source: DataSource = Field(
        default=DataSource.YAHOO,
        description="Data source to use"
    )


class BulkImportRequest(BaseModel):
    """Request model for bulk data import."""
    
    symbols: List[str] = Field(
        ...,
        description="List of symbols to import",
        min_items=1,
        max_items=500
    )
    
    data_types: List[DataType] = Field(
        default=[DataType.PRICES],
        description="Types of data to import"
    )
    
    start_date: Optional[date] = Field(
        default=None,
        description="Start date for import"
    )
    
    end_date: Optional[date] = Field(
        default=None,
        description="End date for import"
    )
    
    data_source: DataSource = Field(
        default=DataSource.YAHOO,
        description="Data source to use"
    )
    
    batch_size: int = Field(
        default=50,
        description="Batch size for processing",
        ge=1,
        le=100
    )
    
    update_existing: bool = Field(
        default=False,
        description="Update existing records"
    )


class DataQualityRequest(BaseModel):
    """Request model for data quality checks."""
    
    symbols: Optional[List[str]] = Field(
        default=None,
        description="Symbols to check (all if None)"
    )
    
    start_date: Optional[date] = Field(
        default=None,
        description="Start date for quality check"
    )
    
    end_date: Optional[date] = Field(
        default=None,
        description="End date for quality check"
    )
    
    check_gaps: bool = Field(
        default=True,
        description="Check for data gaps"
    )
    
    check_outliers: bool = Field(
        default=True,
        description="Check for outliers"
    )
    
    check_duplicates: bool = Field(
        default=True,
        description="Check for duplicates"
    )
