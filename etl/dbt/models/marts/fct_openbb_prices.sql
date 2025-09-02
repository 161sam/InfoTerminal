{{ config(materialized='view') }}
select
  as_of_date,
  symbol,
  open, high, low, close, volume
from {{ source('openbb','stg_openbb_prices') }}
