from django.test import TestCase, override_settings
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch, Mock
import json

from ..models import Stock


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AlphaVantageIntegrationTests(TestCase):
    """Test AlphaVantage API integration with mocking"""

    # Relying on seeded data (for now) because backend methods currently default to the seeded portfolio
    fixtures = ['initdata.json']

    @patch('tracker_app.views.requests.get')
    def test_stock_search(self, mock_get):
        """Test stock search via AlphaVantage API"""
        # Mock the API response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Meta Data": {
                "3. Last Refreshed": "2024-01-15 16:00:00",
                "6. Time Zone": "US/Eastern"
            },
            "Time Series (1min)": {
                "2024-01-15 16:00:00": {
                    "4. close": "155.50"
                }
            }
        })
        mock_get.return_value = mock_response

        url = reverse('stock-index')
        response = self.client.get(url, {'symbol': 'AAPL'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AAPL')
        self.assertContains(response, '155.50')

    @patch('tracker_app.views.requests.get')
    def test_update_portfolio_prices(self, mock_get):
        """Test updating portfolio stock prices from AlphaVantage"""
        # Mock the API response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Meta Data": {
                "3. Last Refreshed": "2024-01-15 16:00:00",
                "6. Time Zone": "US/Eastern"
            },
            "Time Series (1min)": {
                "2024-01-15 16:00:00": {
                    "4. close": "160.25"
                }
            }
        })
        mock_get.return_value = mock_response

        url = reverse('update-seeded-portfolio')
        response = self.client.get(url)

        # Should redirect to home page
        self.assertEqual(response.status_code, 302)

        # Check that stock price was updated
        stock = Stock.objects.get(symbol="AAPL")
        self.assertEqual(stock.last_trade_price, Decimal("160.250"))
