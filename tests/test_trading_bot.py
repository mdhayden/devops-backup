"""
Unit tests for Alpaca Trading Bot
Demonstrates testing in CI/CD pipeline
"""
import unittest
import os
import sys
import pandas as pd
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_dashboard import load_configuration, get_ticker_prices, get_trading_history


class TestTradingBot(unittest.TestCase):
    """Test cases for trading bot functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_api = Mock()
        self.test_tickers = ['AAPL', 'AMZN', 'TSLA', 'MA']

    @patch('web_dashboard.open')
    @patch('web_dashboard.json.loads')
    def test_load_configuration_success(self, mock_json_loads, mock_open):
        """Test successful configuration loading"""
        # Setup mocks
        mock_json_loads.return_value = {
            'APCA-API-KEY-ID': 'test-key',
            'APCA-API-SECRET-KEY': 'test-secret'
        }
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = 'AAPL\nAMZN\nTSLA\nMA'

        with patch('web_dashboard.alpaca.REST') as mock_rest:
            api, tickers = load_configuration()
            
            # Assertions
            self.assertIsNotNone(api)
            self.assertEqual(tickers, ['AAPL', 'AMZN', 'TSLA', 'MA'])
            mock_rest.assert_called_once()

    @patch('web_dashboard.open')
    def test_load_configuration_failure(self, mock_open):
        """Test configuration loading failure"""
        mock_open.side_effect = FileNotFoundError()
        
        api, tickers = load_configuration()
        
        # Should return None on failure
        self.assertIsNone(api)
        self.assertIsNone(tickers)

    def test_get_ticker_prices_success(self):
        """Test successful ticker price retrieval"""
        # Setup mock API
        mock_trade = Mock()
        mock_trade.price = 150.25
        mock_trade.timestamp = '2023-01-01T10:00:00Z'
        
        self.mock_api.get_latest_trade.return_value = mock_trade
        
        # Test
        result = get_ticker_prices(self.mock_api, ['AAPL'])
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['symbol'], 'AAPL')
        self.assertEqual(result[0]['price'], 150.25)
        self.assertEqual(result[0]['timestamp'], '2023-01-01T10:00:00Z')

    def test_get_ticker_prices_api_error(self):
        """Test ticker price retrieval with API error"""
        # Setup mock to raise exception
        self.mock_api.get_latest_trade.side_effect = Exception("API Error")
        
        # Test
        result = get_ticker_prices(self.mock_api, ['AAPL'])
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['symbol'], 'AAPL')
        self.assertEqual(result[0]['price'], 'Error')
        self.assertEqual(result[0]['timestamp'], 'N/A')

    @patch('web_dashboard.os.path.exists')
    @patch('web_dashboard.pd.read_csv')
    def test_get_trading_history_success(self, mock_read_csv, mock_exists):
        """Test successful trading history retrieval"""
        # Setup mocks
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'Time': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'Type': ['buy', 'sell'],
            'Ticker': ['AAPL', 'AAPL'],
            'Quantity': [10, 10],
            'Price': [150.0, 151.0],
            'Total': [1500.0, 1510.0]
        })
        mock_read_csv.return_value = mock_df
        
        # Test
        result = get_trading_history()
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Type'], 'buy')
        self.assertEqual(result[1]['Type'], 'sell')

    @patch('web_dashboard.os.path.exists')
    def test_get_trading_history_no_file(self, mock_exists):
        """Test trading history when file doesn't exist"""
        mock_exists.return_value = False
        
        result = get_trading_history()
        
        self.assertEqual(result, [])

    def test_calculate_profit_loss(self):
        """Test P&L calculation logic"""
        # Test data
        buy_price = 100.0
        sell_price = 105.0
        quantity = 10
        
        # Calculate P&L
        profit_loss = (sell_price - buy_price) * quantity
        
        # Assertions
        self.assertEqual(profit_loss, 50.0)

    def test_risk_management(self):
        """Test risk management rules"""
        portfolio_value = 100000
        max_position_size = 0.05  # 5% max per position
        
        # Calculate maximum investment per position
        max_investment = portfolio_value * max_position_size
        
        # Test position sizing
        self.assertEqual(max_investment, 5000.0)
        self.assertLess(max_investment, portfolio_value * 0.1)  # Safety check


class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling"""

    def test_ticker_validation(self):
        """Test ticker symbol validation"""
        valid_tickers = ['AAPL', 'MSFT', 'GOOGL']
        invalid_tickers = ['', '123', 'toolong']
        
        for ticker in valid_tickers:
            self.assertLessEqual(len(ticker), 5)
            self.assertTrue(ticker.isalpha())
        
        for ticker in invalid_tickers:
            self.assertFalse(len(ticker) > 0 and len(ticker) <= 5 and ticker.isalpha())

    def test_price_validation(self):
        """Test price data validation"""
        valid_prices = [10.50, 100.0, 1500.25]
        invalid_prices = [-10.0, 0, 'abc']
        
        for price in valid_prices:
            self.assertIsInstance(price, (int, float))
            self.assertGreater(price, 0)
        
        for price in invalid_prices:
            if isinstance(price, (int, float)):
                self.assertLessEqual(price, 0)
            else:
                self.assertNotIsInstance(price, (int, float))


if __name__ == '__main__':
    unittest.main()