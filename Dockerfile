FROM python:3.11.4-slim-bullseye

RUN pip install --no-cache-dir \
    poetry==1.5.1 && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY . /app/

RUN poetry install --no-dev --no-root

ENTRYPOINT [ "python", "gas_prices_gr/scrape_gas_prices_vrisko.py" ]
