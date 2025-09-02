{{ config(materialized='table') }}
with sym as (
  select distinct lower(symbol) as symbol
  from {{ ref('stg_openbb_prices') }}
)
select
  {{ dbt_utils.generate_surrogate_key(['symbol']) }} as asset_id,
  symbol
from sym
