{{ config(materialized='view') }}
select
  cast(as_of_date as date)          as as_of_date,
  trim(symbol)                       as symbol,
  cast(open as double precision)     as open,
  cast(high as double precision)     as high,
  cast(low as double precision)      as low,
  cast(close as double precision)    as close,
  cast(volume as bigint)             as volume,
  vendor_ts
from {{ source('openbb','stg_openbb_prices') }}
