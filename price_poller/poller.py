import asyncio
from collections import deque
from datetime import datetime, timezone

import aiohttp
from aiohttp import ClientSession

from configs.configuration import API_URL, API_PARAMS, MAX_RETRIES
from logger import setup_logger


class BTCPricePoller:

    def __init__(self):
        self.running = True
        self.price_history = deque(maxlen=10)
        self.logger = setup_logger("btc_price_poller", "btc_price_poller.log")

    @staticmethod
    def get_simple_average(prices):
        return sum(prices) / len(prices) if prices else 0.0

    @staticmethod
    def parse_price_response(data: dict) -> tuple:
        """
        Method to parse price response

        :param data: dict
        :return: tuple
        """
        price = data["bitcoin"]["usd"]
        timestamp = data["bitcoin"]["last_updated_at"]
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
        return dt, price

    async def fetch_price(self, session, limit=0) -> None:
        """
        Method to fetch price from API response

        :param limit: int, default=0
        :param session: session
        :return: None
        """
        backoff = 1
        failures = 0
        count = 0

        while self.running:
            while self.running:
                if limit is not None and count >= limit:
                    break
            try:
                async with session.get(API_URL, params=API_PARAMS) as response:
                    if response.status >= 500:
                        raise Exception(f"Server error: HTTP {response.status}")
                    response.raise_for_status()
                    data = await response.json()
                    dt, price = self.parse_price_response(data)
                    self.price_history.append(price)
                    sma = self.get_simple_average(self.price_history)
                    print(f"[{dt}] BTC → USD: ${price:,.2f} | SMA(10): ${sma:,.2f}")
                    failures = 0
                    backoff = 1
            except Exception as e:
                failures += 1
                self.logger.error(f"Fetch attempt {failures} failed: {e}")
                if failures <= MAX_RETRIES:
                    print(f"Error: {e}. Retrying in {backoff}s...")
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    self.logger.error("Max retries exceeded. Last error:{e}}")
                    print("Max retries exceeded. Logging error and continuing polling.")
                    failures = 0
                    backoff = 1
            await asyncio.sleep(2)
            count += 1
