FROM python:3.11.4-slim-bullseye as base

WORKDIR /build

COPY . .

# hadolint ignore=SC2094
RUN pip install --no-cache-dir \
    poetry==1.5.1 && \
    poetry config virtualenvs.create false && \
    poetry export -f requirements.txt > requirements.txt

FROM python:3.11.4-slim-bullseye as prod

COPY --from=base /build/requirements.txt /app/requirements.txt
COPY --from=base /build/gas_prices_gr /app/gas_prices_gr/

RUN pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf \
    /usr/local/lib/python3.11/site-packages/setuptools \
    /var/cache/debconf/templates.da* \
    /var/lib/apt/lists/*

ENTRYPOINT [ "python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "app.gas_prices_gr.scrape_gas_prices_vrisko:app"]
