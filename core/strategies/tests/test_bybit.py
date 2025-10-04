import unittest
from unittest.mock import patch, Mock
from core.execution.bybit import BybitAPI

@patch.dict('os.environ', {'BYBIT_API_KEY': 'test_key', 'BYBIT_API_SECRET': 'test_secret'})
class TestBybitAPI(unittest.TestCase):

    @patch('core.execution.bybit.HTTP')
    def test_get_market_data(self, mock_http):
        # Mock the API response
        mock_http.return_value.get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct method was called
        mock_http.return_value.get_kline.assert_called_with(
            category="spot",
            symbol="BTCUSDT",
            interval="1",
            limit=200
        )

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch('core.execution.bybit.HTTP')
    def test_execute_order(self, mock_http):
        # Mock the API response
        mock_http.return_value.place_order.return_value = {"result": {"orderId": "12345"}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct method was called
        mock_http.return_value.place_order.assert_called_with(
            category="spot",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty="0.01"
        )

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})

if __name__ == '__main__':
    unittest.main()
