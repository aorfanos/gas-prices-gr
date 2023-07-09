FROM python:3.11.4-slim-bullseye

RUN pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY . /app/

RUN poetry install --no-dev --no-root

ENTRYPOINT [ "python", "scrape_gas_prices_vrisko.py" ]
