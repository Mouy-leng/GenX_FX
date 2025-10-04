import unittest
from unittest.mock import patch, Mock
from core.execution.bybit import BybitAPI

@patch.dict('os.environ', {"BYBIT_API_KEY": "test_key", "BYBIT_API_SECRET": "test_secret"})
class TestBybitAPI(unittest.TestCase):

    @patch('core.execution.bybit.HTTP')
    def test_get_market_data(self, MockHTTP):
        # Arrange
        mock_session = MockHTTP.return_value
        mock_session.get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        # Act
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert
        MockHTTP.assert_called_once_with(testnet=False, api_key="test_key", api_secret="test_secret")
        mock_session.get_kline.assert_called_once_with(
            category="spot",
            symbol="BTCUSDT",
            interval="1",
            limit=200
        )
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch('core.execution.bybit.HTTP')
    def test_execute_order(self, MockHTTP):
        # Arrange
        mock_session = MockHTTP.return_value
        mock_session.place_order.return_value = {"result": {"orderId": "12345"}}

        # Act
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert
        MockHTTP.assert_called_once_with(testnet=False, api_key="test_key", api_secret="test_secret")
        mock_session.place_order.assert_called_once_with(
            category="spot",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty="0.01",
        )
        self.assertEqual(result, {"result": {"orderId": "12345"}})

if __name__ == '__main__':
    unittest.main()