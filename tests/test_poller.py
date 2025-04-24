import pytest
from datetime import datetime, timezone

from price_poller.poller import BTCPricePoller

import aiohttp

test_data = [
    (
        {
            "bitcoin": {
                "usd": 41000.0,
                "last_updated_at": 1618883984
            }
        },
        datetime.fromtimestamp(1618883984, tz=timezone.utc).isoformat(),
        41000.0
    ),
    (
        {
            "bitcoin": {
                "usd": 32000.5,
                "last_updated_at": 1633024800
            }
        },
        datetime.fromtimestamp(1633024800, tz=timezone.utc).isoformat(),
        32000.5
    ),
    (
        {
            "bitcoin": {
                "usd": 0.0,
                "last_updated_at": 1628883984
            }
        },
        datetime.fromtimestamp(1628883984, tz=timezone.utc).isoformat(),
        0.0
    ),
]


@pytest.mark.parametrize("data, expected_dt, expected_price", test_data)
def test_parse_price_response(data, expected_dt, expected_price):
    """
    Test parse_price_response with different inputs
    """
    dt, price = BTCPricePoller.parse_price_response(data)

    assert dt == expected_dt
    assert price == expected_price
