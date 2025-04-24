import asyncio
from datetime import datetime, timezone

import aiohttp
from aiohttp import ClientSession

from configs.configuration import API_URL, API_PARAMS


class BTCPricePoller:

    def __init__(self):
        self.running = True

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
                    print(f"[{dt}] BTC → USD: ${price:,.2f}")
            except Exception as e:
                print("Failed to fetch BTC price", e)
            await asyncio.sleep(1)
            count += 1
