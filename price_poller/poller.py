import asyncio
from collections import deque
from datetime import datetime, timezone

import aiohttp
from aiohttp import ClientSession

from configs.configuration import API_URL, API_PARAMS, MAX_RETRIES
from logger import setup_logger


class CoinPricePoller:

    def __init__(self, coin: str='bitcoin'):
        self.coin = coin
        self.running = True
        self.price_history = deque(maxlen=10)
        self.logger = setup_logger("btc_price_poller",
                                   "btc_price_poller.log")
        API_PARAMS['ids'] = self.coin


    @staticmethod
    def compute_average_of_ten(prices: deque[float]) -> float:
        """
        Method to commute average of 10 prices

        :param prices: deque[float]
        :return: float
        """
        return sum(prices) / len(prices) if prices else 0.0

    def parse_price_response(self, data: dict) -> tuple:
        """
        Method to parse price response
        """
        price = data[self.coin]["usd"]
        timestamp = data[self.coin]["last_updated_at"]
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
        return dt, price

    async def fetch_price(self, session, limit: int = None) -> None:
        """
        Method to fetch price from API response
        """
        backoff = 1
        failures = 0
        count = 0

        while self.running:
            if limit is not None and count >= limit:
                break
            try:
                async with session.get(API_URL, params=API_PARAMS) as response:
                    if response.status >= 500:
                        raise Exception(f"Server error: HTTP {response.status}")
                    response.raise_for_status()
                    data: dict = await response.json()
                    dt, price = self.parse_price_response(data)
                    self.price_history.append(price)
                    sma = self.compute_average_of_ten(self.price_history)
                    print(f"[{dt}] {self.coin} → USD: ${price:,.2f} | SMA(10): ${sma:,.2f}")
                    failures = 0
                    backoff = 1
            except Exception as e:
                failures += 1
                print(f"Fetch attempt {failures} failed")
                if failures <= MAX_RETRIES:
                    print(f"Error: {e}. Retrying in {backoff}s...")
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    self.logger.error(f"Max retries exceeded. Last error: {e}")
                    print("Max retries exceeded. Logging error and continuing polling.")
                    failures = 0
                    backoff = 1

            await asyncio.sleep(1)
            count += 1

    def stop(self):
        """ Method to stop tasks"""
        self.running = False
