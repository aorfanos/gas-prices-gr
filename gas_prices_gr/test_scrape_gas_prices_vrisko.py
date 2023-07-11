import unittest
from gas_prices_gr.scrape_gas_prices_vrisko import\
    extract_gas_price,\
    get_gas_stations_fullpage_for_location_html


class TestScrapeGasPrices(unittest.TestCase):
    def test_get_gas_stations_fullpage_for_location_html_valid(self):
        # Test a valid location
        location = 'athina'
        result = get_gas_stations_fullpage_for_location_html(location)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bytes)

    def test_get_gas_stations_fullpage_for_location_html_invalid(self):
        # Test an invalid location
        location = 'invalid_location'
        result = get_gas_stations_fullpage_for_location_html(location)
        self.assertIsNone(result)


class TestExtractGasPrice(unittest.TestCase):
    def test_extract_gas_price_with_comma_separator(self):
        gas_station_fueltype_string = 'Unleaded 95: 1,50 €'
        expected_price = 1.50
        actual_price = extract_gas_price(gas_station_fueltype_string)
        self.assertEqual(actual_price, expected_price)

    def test_extract_gas_price_with_period_separator(self):
        gas_station_fueltype_string = 'Unleaded 95: 1.5 €'
        expected_price = 0
        actual_price = extract_gas_price(gas_station_fueltype_string)
        self.assertEqual(actual_price, expected_price)

    def test_extract_gas_price_with_no_price(self):
        gas_station_fueltype_string = 'Unleaded 95: N/A'
        expected_price = 0
        actual_price = extract_gas_price(gas_station_fueltype_string)
        self.assertEqual(actual_price, expected_price)

    def test_extract_gas_price_with_no_match(self):
        gas_station_fueltype_string = 'Unleaded 95'
        expected_price = 0
        actual_price = extract_gas_price(gas_station_fueltype_string)
        self.assertEqual(actual_price, expected_price)


if __name__ == '__main__':
    unittest.main()
