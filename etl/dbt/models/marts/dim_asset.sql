select symbol as asset_key, name from {{ ref('stg_assets') }}
