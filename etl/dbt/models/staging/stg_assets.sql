select symbol, name
from {{ ref('assets') }}
