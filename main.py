import asyncio
import signal
import sys

import aiohttp

from price_poller.poller import BTCPricePoller

poller = BTCPricePoller()


async def shutdown(sig, loop, stop_event):
    print(f"Shutting down...")
    poller.stop()

    stop_event.set()

    # Cansel all tasks exclude current
    tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def main():
    """ Main """
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    # Use signal.signal for Windows - Ctrl+C
    if sys.platform == "win32":
        signal.signal(signal.SIGINT, lambda sig, frame: asyncio.create_task(shutdown(sig, loop, stop_event)))
    else:
        # For Linux and macOS used loop.add_signal_handler
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(signal.SIGINT, loop, stop_event)))

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            poller.fetch_price(session),
            stop_event.wait()  # await stop signal
        )


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except asyncio.CancelledError:
        pass
