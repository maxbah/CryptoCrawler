import asyncio

import aiohttp

from price_poller.poller import BTCPricePoller

poller = BTCPricePoller()


async def main():
    async with aiohttp.ClientSession() as session:
        await poller.fetch_price(session)


if __name__ == "__main__":
    asyncio.run(main())
