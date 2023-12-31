import requests
import re
import json

from bs4 import BeautifulSoup
from flask import Flask, make_response
from .utils import extract_date, greek_date_to_ts
from .gas_station_enum import find_gas_station_company

FAKE_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'


headers = {
    'User-Agent': FAKE_UA,
}

# >> Flask app init << #
app = Flask(__name__)


def get_gas_stations_fullpage_for_location_html(location):
    """Returns the full page html for a given location."""
    response = requests.get(
        f'https://www.vrisko.gr/times-kafsimon-venzinadika/{location}', headers=headers,
    )
    if response.status_code == 200:
        return response.content
    else:
        return None


def get_gas_stations_full(fullpage_html):
    data = {}
    if fullpage_html is None:
        srv_response = make_response('Location not found for vrisko', 404)
        srv_response.status_code = 404
        return srv_response
    soup = BeautifulSoup(fullpage_html, 'html.parser')
    gas_station_names = soup.find_all('div', class_='GasCompanyName')
    gs_names_list = []
    gas_station_addr = soup.find_all('div', class_='GasAddress')
    gs_addr_list = []
    gas_result_footer = soup.find_all('div', class_='GasResultFooter')
    gas_result_last_update = soup.find_all('div', class_='GasResultLastUpdate')
    icon_span = soup.find_all('span', class_='GasResultLastUpdateIcon')

    gs_unl_95_list = []
    gs_unl_100_list = []
    gs_auto_gas_list = []
    gs_auto_diesel_list = []
    gs_heating_oil_list = []
    gs_heating_oil_lt_1000lt_list = []
    last_update_date_list = []
    icon_span_list = []

    for i, gas_station_name in enumerate(gas_station_names):
        gas_station_names[i] = gas_station_name.text
        gs_names_list.append(gas_station_name.text)
        # print(gas_station_names[i])

    for i, gas_station_addr in enumerate(gas_station_addr):
        gas_station_addr[i] = gas_station_addr.text
        gs_addr_list.append(gas_station_addr.text)
        # print(gas_station_addr[i])

    for gas_result in gas_result_footer:
        # >> Unleaded 95 << #
        unl_95_name = gas_result.find('div', class_='unleaded-95')
        for i, unl_95 in enumerate(unl_95_name):
            gs_unl_95_list.append(
                extract_gas_price(
                    unl_95_name.b.string.strip(),
                ),
            )
        # >> Unleaded 100 << #
        unl_100_name = gas_result.find('div', class_='unleaded-100')
        for i, unl_100 in enumerate(unl_100_name):
            gs_unl_100_list.append(
                extract_gas_price(
                    unl_100_name.b.string.strip(),
                ),
            )
        # >> Auto Gas << #
        auto_gas_name = gas_result.find('div', class_='auto-gas')
        for i, auto_gas in enumerate(auto_gas_name):
            gs_auto_gas_list.append(
                extract_gas_price(
                    auto_gas_name.b.string.strip(),
                ),
            )
        # >> Auto Diesel << #
        auto_diesel_name = gas_result.find('div', class_='diesel-vehicles')
        for i, auto_diesel in enumerate(auto_diesel_name):
            gs_auto_diesel_list.append(
                extract_gas_price(
                    auto_diesel_name.b.string.strip(),
                ),
            )
        # >> Heating Oil << #
        heating_oil_name = gas_result.find('div', class_='diesel-heating')
        for i, heating_oil in enumerate(heating_oil_name):
            gs_heating_oil_list.append(
                extract_gas_price(
                    heating_oil_name.b.string.strip(),
                ),
            )
        # >> Diesel > 1000lt << #
        heating_oil_lt_1000lt_name = gas_result.find(
            'div', class_='diesel-delivery',
        )
        for i, heating_oil_lt_1000lt in enumerate(heating_oil_lt_1000lt_name):
            gs_heating_oil_lt_1000lt_list.append(
                extract_gas_price(
                    heating_oil_lt_1000lt_name.b.string.strip(),
                ),
            )

    for gas_result in gas_result_last_update:
        last_update_date_gr = extract_date(gas_result.text)
        last_update_date_list.append(last_update_date_gr)

    for i, icon in enumerate(icon_span):
        icon_span_list.append(find_gas_station_company(icon.span.get('class')))

        # >> Produce result JSON << #
    for i in range(len(gas_station_names)):
        data[gas_station_names[i]] = {
            'name': gs_names_list[i],
            'address': gs_addr_list[i],
            'company': icon_span_list[i],
            'last_update_ts': greek_date_to_ts(last_update_date_list[i]),
            'fuel_prices': {
                'unleaded_95': gs_unl_95_list[i],
                'unleaded_100': gs_unl_100_list[i],
                'auto_gas': gs_auto_gas_list[i],
                'auto_diesel': gs_auto_diesel_list[i],
                'heating_oil': gs_heating_oil_list[i],
                'heating_oil_lt_1000lt': gs_heating_oil_lt_1000lt_list[i],
            },
        }

    return json.dumps(data)


def extract_gas_price(gas_station_fueltype_string):
    """Extracts the gas price from the gas station fuel prices."""
    pattern = r'\d{1,3}(,\d{1,3})'
    match = re.search(pattern, gas_station_fueltype_string)
    if match:
        return float(match.group().replace(',', '.'))
    else:
        return 0


# >> Flask << #
# dynamic route ref:
# https://www.geeksforgeeks.org/generating-dynamic-urls-in-flask/
@ app.route('/scrape/vrisko/<string:Location>')
def scrape_vriskogr(Location):
    main_page_html = get_gas_stations_fullpage_for_location_html(Location)
    return get_gas_stations_full(main_page_html)


@ app.route('/')
def index():
    return 'Fuel prices GR API'


@ app.route('/scrape/ready')
def scrape_ready():
    main_page_html = get_gas_stations_fullpage_for_location_html('athina')
    if main_page_html is not None:
        return 'Ready'


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 5000, app)
    httpd.serve_forever()
