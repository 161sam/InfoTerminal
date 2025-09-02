{{ config(materialized='table', tags=['openbb']) }}
select
  d.asset_id,
  s.as_of_date,
  s.open, s.high, s.low, s.close, s.volume
from {{ ref('stg_openbb_prices') }} s
join {{ ref('dim_asset') }} d
  on lower(s.symbol) = d.symbol
