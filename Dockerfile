FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

COPY README.md /app/

RUN poetry install --no-root

COPY . /app/

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "python", "main.py"]