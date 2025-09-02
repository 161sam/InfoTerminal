-- TODO: mappe OpenBB-Rohdaten in saubere Staging-Spalten
select * from {{ source('openbb','prices_raw') }}
