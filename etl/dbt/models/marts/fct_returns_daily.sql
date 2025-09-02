{{ config(materialized='table') }}
with base as (
  select asset_id, as_of_date, close,
         lag(close) over (partition by asset_id order by as_of_date) as prev_close
  from {{ ref('fct_eod_prices') }}
)
select
  asset_id, as_of_date,
  close,
  case when prev_close is null or prev_close = 0 then null
       else (close - prev_close) / prev_close end as ret_d
from base
