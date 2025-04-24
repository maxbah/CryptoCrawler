# Price poller API
API_URL = "https://api.coingecko.com/api/v3/simple/price"
API_PARAMS = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_last_updated_at": "true"
    }
MAX_RETRIES = 5