{{ config(materialized='view') }}
select
  d.asset_id, d.symbol, s.isin
from {{ ref('dim_asset') }} d
left join {{ ref('asset_ref') }} s
  on upper(d.symbol) = s.symbol
