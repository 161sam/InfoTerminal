"""
DEPRECATED: Legacy OpenBB Connector Script

This file is DEPRECATED and will be removed in a future version.
Use app_v1.py instead which provides:

- Full REST API with /v1 endpoints
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Background job processing
- Symbol information retrieval
- Data quality checks
- Statistics and monitoring

Migration Guide:
- Replace direct script execution with API calls
- Use /v1/prices/fetch for data import
- Use /v1/symbols for symbol management
- Use /v1/statistics for monitoring
- Enhanced error handling and logging

For new integrations, use app_v1.py API directly.
"""

import warnings
import sys
import os

# Issue deprecation warning
warnings.warn(
    "openbb-connector/main.py is deprecated. Use app_v1.py for the full REST API. "
    "This legacy script will be removed in the next major version.",
    DeprecationWarning,
    stacklevel=2
)

print("WARNING: This is the deprecated OpenBB connector script.", file=sys.stderr)
print("Use 'python app_v1.py' for the standardized v1 API.", file=sys.stderr)
print("For direct data import, use the API endpoint: POST /v1/prices/fetch", file=sys.stderr)
print("", file=sys.stderr)

# Legacy implementation for backward compatibility
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Keep the original environment variables for compatibility
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "infoterminal")
PG_USER = os.getenv("PG_USER", "app")
PG_PASS = os.getenv("PG_PASS", "app")
SYMS = os.getenv("OPENBB_SYMBOLS", "AAPL,MSFT,SAP.DE").split(",")


def fetch_prices_yahoo(symbols):
    """Legacy function - use API endpoint /v1/prices/fetch instead."""
    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
        sys.exit(1)
    
    print(f"DEPRECATED: Fetching data for {len(symbols)} symbols using legacy script", file=sys.stderr)
    print("RECOMMENDED: Use API endpoint POST /v1/prices/fetch instead", file=sys.stderr)
    
    rows = []
    for s in symbols:
        try:
            hist = yf.download(s, period="5d", interval="1d", progress=False)
            hist = hist.reset_index()
            for _, r in hist.iterrows():
                rows.append({
                    "as_of_date": str(r["Date"].date()),
                    "symbol": s,
                    "open": float(r["Open"]), 
                    "high": float(r["High"]),
                    "low": float(r["Low"]), 
                    "close": float(r["Close"]),
                    "volume": int(r["Volume"])
                })
        except Exception as e:
            print(f"WARN: Failed to fetch data for {s}: {e}", file=sys.stderr)
            continue
    
    return pd.DataFrame(rows)


def ensure_table(conn):
    """Legacy function - database setup now handled by app_v1.py."""
    print("DEPRECATED: Using legacy table setup", file=sys.stderr)
    print("RECOMMENDED: Use app_v1.py which handles database setup automatically", file=sys.stderr)
    
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stg_openbb_prices (
                id SERIAL PRIMARY KEY,
                as_of_date date NOT NULL, 
                symbol text NOT NULL,
                open double precision, 
                high double precision, 
                low double precision, 
                close double precision,
                volume bigint,
                data_source text DEFAULT 'yahoo',
                vendor_ts timestamp default now(),
                UNIQUE(symbol, as_of_date, data_source)
            );
        """)
    conn.commit()


def write_df(conn, df: pd.DataFrame):
    """Legacy function - use API endpoint /v1/prices/fetch with save_to_db=true instead."""
    if df.empty: 
        return
    
    print(f"DEPRECATED: Writing {len(df)} records using legacy method", file=sys.stderr)
    print("RECOMMENDED: Use API endpoint POST /v1/prices/fetch with save_to_db=true", file=sys.stderr)
    
    tpl = [(r.as_of_date, r.symbol, r.open, r.high, r.low, r.close, r.volume) 
           for r in df.itertuples(index=False)]
    
    with conn.cursor() as cur:
        execute_values(cur,
            "INSERT INTO stg_openbb_prices (as_of_date, symbol, open, high, low, close, volume) VALUES %s ON CONFLICT (symbol, as_of_date, data_source) DO NOTHING",
            tpl
        )
    conn.commit()


def main():
    """Legacy main function - use app_v1.py API instead."""
    print("=" * 60, file=sys.stderr)
    print("DEPRECATION NOTICE", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("This legacy OpenBB connector script is deprecated.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Migration to API:", file=sys.stderr)
    print("1. Start the API: python app_v1.py", file=sys.stderr)
    print("2. Use endpoint: POST /v1/prices/fetch", file=sys.stderr)
    print("3. Request body: {", file=sys.stderr)
    print('     "symbols": ["AAPL", "MSFT", "SAP.DE"],', file=sys.stderr)
    print('     "period": "5d",', file=sys.stderr)
    print('     "save_to_db": true', file=sys.stderr)
    print("   }", file=sys.stderr)
    print("", file=sys.stderr)
    print("Benefits of API:", file=sys.stderr)
    print("- Comprehensive error handling", file=sys.stderr)
    print("- Background job processing", file=sys.stderr)
    print("- Data quality validation", file=sys.stderr)
    print("- Statistics and monitoring", file=sys.stderr)
    print("- OpenAPI documentation", file=sys.stderr)
    print("", file=sys.stderr)
    print("Running legacy import for compatibility...", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    try:
        conn = psycopg2.connect(
            host=PG_HOST, 
            port=PG_PORT, 
            dbname=PG_DB, 
            user=PG_USER, 
            password=PG_PASS
        )
        ensure_table(conn)
        
        df = fetch_prices_yahoo(SYMS)
        if df.empty:
            print("ERROR: No data fetched for any symbols", file=sys.stderr)
            sys.exit(1)
        
        write_df(conn, df)
        print(f"SUCCESS: Inserted {len(df)} rows for symbols {SYMS}")
        print("", file=sys.stderr)
        print("NEXT STEPS:", file=sys.stderr)
        print("1. Migrate to app_v1.py API for future imports", file=sys.stderr)
        print("2. See documentation at /docs when running app_v1.py", file=sys.stderr)
        print("3. Use /v1/statistics to monitor data quality", file=sys.stderr)
        
    except Exception as e:
        print(f"ERROR: Import failed: {e}", file=sys.stderr)
        print("", file=sys.stderr)
        print("TROUBLESHOOTING:", file=sys.stderr)
        print("1. Check database connection settings", file=sys.stderr)
        print("2. Ensure yfinance is installed: pip install yfinance", file=sys.stderr)
        print("3. Try the app_v1.py API for better error handling", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
