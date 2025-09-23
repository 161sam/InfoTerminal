"""
InfoTerminal OpenBB Connector Service v1.0.0

Standardized *_v1.py implementation for financial data integration.
Provides unified API for fetching, storing, and analyzing financial market data.

This service replaces the legacy main.py script with:
- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Background job processing
- Database integration
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import psycopg2
import structlog

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    HealthChecker,
    DependencyCheck
)

# Import routers
from routers.core_v1 import router as core_router, set_dependencies
from routers.openbb_v1 import router as openbb_router, set_openbb_system

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Service Configuration
SERVICE_NAME = "openbb-connector"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "Financial data connector using OpenBB and various data sources for comprehensive market analysis"

# Database Configuration
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "infoterminal")
PG_USER = os.getenv("PG_USER", "app")
PG_PASS = os.getenv("PG_PASS", "app")

# OpenBB Configuration
DEFAULT_SYMBOLS = os.getenv("OPENBB_SYMBOLS", "AAPL,MSFT,SAP.DE").split(",")
ENABLE_AUTO_IMPORT = os.getenv("OPENBB_AUTO_IMPORT", "0") == "1"
IMPORT_INTERVAL_HOURS = int(os.getenv("OPENBB_IMPORT_INTERVAL", "24"))

# Global state
db_connection = None
data_sources = {}
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)


def check_database_connection() -> DependencyCheck:
    """Check database connection health."""
    try:
        if db_connection is None:
            return DependencyCheck(
                status="unhealthy",
                error="Database connection not initialized"
            )
        
        # Test connection
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return DependencyCheck(
            status="healthy",
            message="Database connection active",
            latency_ms=5.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=f"Database connection failed: {str(e)}"
        )


def check_data_sources() -> DependencyCheck:
    """Check data source availability."""
    try:
        # Check Yahoo Finance availability (basic check)
        import yfinance as yf
        
        # Try to fetch a simple ticker
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        
        if info and "symbol" in info:
            return DependencyCheck(
                status="healthy",
                message="Yahoo Finance data source available",
                latency_ms=100.0
            )
        else:
            return DependencyCheck(
                status="degraded",
                message="Yahoo Finance responding but data quality unclear"
            )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=f"Data source check failed: {str(e)}"
        )


def setup_data_sources():
    """Initialize data source configurations."""
    global data_sources
    
    data_sources = {
        "yahoo": {
            "enabled": True,
            "type": "yahoo_finance",
            "description": "Yahoo Finance API",
            "rate_limit": "2000/hour",
            "supports": ["prices", "info", "dividends", "splits"]
        },
        "alpha_vantage": {
            "enabled": False,
            "type": "alpha_vantage",
            "description": "Alpha Vantage API",
            "api_key_required": True,
            "supports": ["prices", "fundamentals", "forex"]
        },
        "quandl": {
            "enabled": False,
            "type": "quandl",
            "description": "Quandl Financial Data",
            "api_key_required": True,
            "supports": ["economic_data", "commodities"]
        }
    }
    
    # Enable additional sources based on environment variables
    if os.getenv("ALPHA_VANTAGE_API_KEY"):
        data_sources["alpha_vantage"]["enabled"] = True
        data_sources["alpha_vantage"]["api_key"] = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if os.getenv("QUANDL_API_KEY"):
        data_sources["quandl"]["enabled"] = True
        data_sources["quandl"]["api_key"] = os.getenv("QUANDL_API_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global db_connection
    
    logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    try:
        # Initialize database connection
        try:
            db_connection = psycopg2.connect(
                host=PG_HOST,
                port=PG_PORT,
                dbname=PG_DB,
                user=PG_USER,
                password=PG_PASS
            )
            db_connection.autocommit = False
            
            logger.info("Database connection established", 
                       host=PG_HOST, port=PG_PORT, database=PG_DB)
            
            # Ensure price table exists
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
            logger.error("Database initialization failed", error=str(e))
            raise
        
        # Setup data sources
        setup_data_sources()
        logger.info("Data sources configured", 
                   enabled_sources=[name for name, config in data_sources.items() if config["enabled"]])
        
        # Set up dependency checks
        health_checker.add_dependency("database", check_database_connection)
        health_checker.add_dependency("data_sources", check_data_sources)
        
        # Set dependencies in routers
        set_dependencies(db_connection, data_sources)
        set_openbb_system(db_connection, data_sources)
        
        logger.info(f"{SERVICE_NAME} startup completed successfully")
        
    except Exception as e:
        logger.error("Failed to initialize OpenBB connector", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {SERVICE_NAME}")
    
    # Close database connection
    if db_connection:
        try:
            db_connection.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error("Error closing database connection", error=str(e))


# FastAPI application with standardized configuration
app = FastAPI(
    title="InfoTerminal OpenBB Connector API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply standard middleware and exception handlers
setup_standard_middleware(app, SERVICE_NAME)
setup_standard_exception_handlers(app)

# Set up standard OpenAPI documentation
setup_standard_openapi(
    app=app,
    title="InfoTerminal OpenBB Connector API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    service_name=SERVICE_NAME,
    tags_metadata=get_service_tags_metadata(SERVICE_NAME)
)

# Include routers
app.include_router(core_router, tags=["Core"])
app.include_router(openbb_router, prefix="/v1", tags=["Financial Data"])

# Legacy endpoint for backward compatibility with the original script
@app.post("/legacy/import", deprecated=True, include_in_schema=False)
def legacy_import():
    """DEPRECATED: Use /v1/prices/fetch instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/prices/fetch"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/prices/fetch instead"}
    )


# Root endpoint
@app.get("/", include_in_schema=False)
def root():
    """Root endpoint with service information."""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "documentation": "/docs",
        "health_check": "/healthz",
        "readiness_check": "/readyz",
        "openapi_spec": "/openapi.json",
        "features": {
            "supported_data_sources": list(data_sources.keys()) if data_sources else [],
            "database_integration": True,
            "background_jobs": True,
            "data_quality_checks": True,
            "bulk_operations": True,
            "default_symbols": DEFAULT_SYMBOLS,
            "auto_import": ENABLE_AUTO_IMPORT
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app_v1:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
