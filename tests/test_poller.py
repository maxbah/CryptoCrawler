from collections import deque
from datetime import datetime, timezone

import aiohttp
import pytest

from price_poller.poller import CoinPricePoller

@pytest.mark.parametrize(
    "prices, expected_average",
    [
        (deque([10.0, 20.0, 30.0]), 20.0),  # Normal case with 3 prices
        (deque([10.0]), 10.0),  # Only one price
        (deque([]), 0.0),  # Empty deque
        (deque([5.0] * 10), 5.0),  # Exactly 10 prices
    ]
)
def test_compute_average_of_ten(prices, expected_average):
    """Test the compute average of ten """
    result = CoinPricePoller.compute_average_of_ten(prices)
    assert result == expected_average

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
    dt, price = CoinPricePoller().parse_price_response(data)

    assert dt == expected_dt
    assert price == expected_price

def test_stop_method():
    """Test the stop method """
    instance = CoinPricePoller()
    instance.running = True
    instance.stop()
    assert instance.running is False
