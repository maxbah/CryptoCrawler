# CryptoCrawler

Live Bitcoin price poller with simple moving average and retry logic

A Python tool that polls the [CoinGecko API](https://www.coingecko.com/en/api)
every second to retrieve the current price of Bitcoin (BTC) in USD,
displays a (SMA - simple moving average) of the last 10 prices,
and handles errors with exponential backoff.

---

## Developed by

Bakhovskyi Maksym - python software developer

---

## Features

- Fetch BTC→USD price every second
- Compute and display BTC single average(10)
- Retry on network or server errors with exponential backoff
- Gracefully handle Ctrl+C (SIGINT)
- Logs errors to btc_price_poller.log

---

## Requirements

- Python 3.9+
- Poetry
- Internet connection (for live API calls)

---

## Installation

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Poetry install
pip install poetry

# Poetry actions
poetry install
poetry update 
```
## Run

```bash
python main.py
```

## Exit
```bash
ctrl+C
```