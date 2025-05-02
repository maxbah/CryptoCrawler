# CryptoCrawler

Live Coins (by default=Bitcoin) price poller with simple moving average and retry logic

A Python tool that polls the [CoinGecko API](https://www.coingecko.com/en/api)
every interval in seconds to retrieve the current price of coin (default=Bitcoin) in USD, 
but there is an option to easily change to another coin or even poll several coins,  
displays a (SMA - simple moving average) of the last 10 prices,
and handles errors with exponential backoff.
Errors save to appropriated log file

---

## Developed by

Bakhovskyi Maksym - python software developer

---

## Features

- Fetch COIN→USD price every interval in seconds
- Compute and display coin single average(10)
- Retry on network or server errors with exponential backoff
- Gracefully handle Ctrl+C (SIGINT)
- Logs errors to f'{coin_name}_price_poller.log'
- Option to easily change to another coin
- Poll several different coins 

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

## Run on Docker (Docker should be installed)
```bash
docker build -t btc_price_poller .
docker run --name=btc_price_poller -p 8000:8000 btc_price_poller
```

# Stop on Docker run

```bash
ctrl+C
```
or stop running docker container

## RUN tests

```bash
pytest
```

