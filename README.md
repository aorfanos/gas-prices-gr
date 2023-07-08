# Scrape Gas Prices Greece API

This is a Python script that scrapes gas prices from
the vrisko.gr website for a given location in Greece,
and outputs the results in JSON format via REST API.

## Requirements

* asdf

## Usage

Running the script will start a server on port 5000.
The server has the following endpoints:

* `/scrape/xegr/<location>`

### Example

```
$ curl http://localhost:5000/scrape/xegr/athina
## Note: you can get the endpoints for the other
locations by visiting the website and
inspecting the network requests
```

Each gas station in the location is represented
by a dictionary with the following keys:

* name: The name of the gas station.
* address: The address of the gas station.
* unleaded_95: The price of unleaded 95 gasoline at the gas station.
* unleaded_100: The price of unleaded 100 gasoline at the gas station.
* auto_gas: The price of auto gas at the gas station.
* auto_diesel: The price of auto diesel at the gas station.
* heating_oil: The price of heating oil at the gas station.
* heating_oil_lt_1000lt: The price of heating oil for quantities > 1000 lt
