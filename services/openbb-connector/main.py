import os, sys, time
import pandas as pd
import requests
import psycopg2
from psycopg2.extras import execute_values

PG_HOST=os.getenv("PG_HOST","localhost")
PG_PORT=int(os.getenv("PG_PORT","5432"))
PG_DB=os.getenv("PG_DB","infoterminal")
PG_USER=os.getenv("PG_USER","app")
PG_PASS=os.getenv("PG_PASS","app")
SYMS=os.getenv("OPENBB_SYMBOLS","AAPL,MSFT,SAP.DE").split(",")

def fetch_prices_yahoo(symbols):
  import yfinance as yf  # requires: pip install yfinance
  rows=[]
  for s in symbols:
    hist = yf.download(s, period="5d", interval="1d", progress=False)
    hist = hist.reset_index()
    for _,r in hist.iterrows():
      rows.append({
        "as_of_date": str(r["Date"].date()),
        "symbol": s,
        "open": float(r["Open"]), "high": float(r["High"]),
        "low": float(r["Low"]), "close": float(r["Close"]),
        "volume": int(r["Volume"])
      })
  return pd.DataFrame(rows)

def ensure_table(conn):
  with conn.cursor() as cur:
    cur.execute("""
      CREATE TABLE IF NOT EXISTS stg_openbb_prices (
        as_of_date date, symbol text,
        open double precision, high double precision, low double precision, close double precision,
        volume bigint,
        vendor_ts timestamp default now()
      );
    """)
  conn.commit()

def write_df(conn, df: pd.DataFrame):
  if df.empty: return
  tpl=[(r.as_of_date, r.symbol, r.open, r.high, r.low, r.close, r.volume) for r in df.itertuples(index=False)]
  with conn.cursor() as cur:
    execute_values(cur,
      "INSERT INTO stg_openbb_prices (as_of_date, symbol, open, high, low, close, volume) VALUES %s",
      tpl
    )
  conn.commit()

def main():
  conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)
  ensure_table(conn)
  try:
    df = fetch_prices_yahoo(SYMS)
  except Exception as e:
    print("fetch failed:", e, file=sys.stderr); sys.exit(2)
  write_df(conn, df)
  print(f"Inserted {len(df)} rows for symbols {SYMS}")

if __name__ == "__main__":
  main()
