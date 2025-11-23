from django.test import TestCase, override_settings
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch, Mock
import json

from ..models import Portfolio, Stock


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AlphaVantageIntegrationTests(TestCase):
    """Test AlphaVantage API integration with mocking"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")

        Stock.objects.create(
            symbol='AAPL',
            portfolio=self.portfolio,
            shares_owned=Decimal('10.000'),
            last_trade_price=Decimal('150.00'),
        )
        Stock.objects.create(
            symbol='GOOGL',
            portfolio=self.portfolio,
            shares_owned=Decimal('5.000'),
            last_trade_price=Decimal('140.00'),
        )

    @patch('tracker_app.views.requests.get')
    def test_single_stock_lookup(self, mock_get):
        """
        Test that stock search (stock lookup) makes a well-formed API call for that stock
        and provides data according to application needs.
        """

        ticker_symbol = 'AAPL'
        current_price = '155.50'

        # Mock the API response
        mock_get.return_value = self._mock_single_stock_api_response(current_price)

        # Call method under test
        url = reverse('stock-index')
        response = self.client.get(url, {'symbol': ticker_symbol, 'portfolio_id': self.portfolio.pk})

        # Verify view returns 200
        self.assertEqual(response.status_code, 200)

        # Verify API was called once
        self.assertEqual(mock_get.call_count, 1)

        # Verify correct API domain and parameters
        call_url = mock_get.call_args[0][0]
        self.assertIn('https://www.alphavantage.co/query', call_url)
        self.assertIn('function=TIME_SERIES_INTRADAY', call_url)
        self.assertIn(f"symbol={ticker_symbol}", call_url)
        self.assertIn('interval=1min', call_url)
        self.assertIn('apikey=', call_url)

        # Verify response contains expected data
        self.assertContains(response, ticker_symbol)
        self.assertContains(response, current_price)

    @patch('tracker_app.views.requests.get')
    def test_refresh_portfolio_prices(self, mock_get):
        """
        Test that refresh makes a well-formed API call for each stock in a portfolio
        and updates the database accordingly.
        """

        # Mock API responses for each stock
        new_prices = {'AAPL': '175.50', 'GOOGL': '155.25'}
        mock_get.side_effect = self._mock_api_response_by_symbol(new_prices)

        # Call method under test
        url = reverse('refresh-portfolio', kwargs={'pk': self.portfolio.pk})
        response = self.client.get(url)

        # Verify view returns redirect (302)
        self.assertEqual(response.status_code, 302)

        # Verify API was called once per stock in portfolio
        expected_call_count = self.portfolio.stock_set.count()
        self.assertEqual(mock_get.call_count, expected_call_count)

        # Verify correct API domain and parameters were used for each stock
        call_urls = [call[0][0] for call in mock_get.call_args_list]
        for call_url in call_urls:
            self.assertIn('https://www.alphavantage.co/query', call_url)
            self.assertIn('function=TIME_SERIES_INTRADAY', call_url)
            self.assertIn('interval=1min', call_url)
            self.assertIn('apikey=', call_url)
        for symbol in new_prices:
            self.assertTrue(any(f'symbol={symbol}' in url for url in call_urls))

        # Verify database was updated with new prices
        for symbol, expected_price in new_prices.items():
            stock = Stock.objects.get(symbol=symbol)
            self.assertEqual(stock.last_trade_price, Decimal(expected_price))

    def _mock_single_stock_api_response(self, price):
        """Return mock response for a single stock API call."""
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Meta Data": {
                "3. Last Refreshed": "2024-01-15 16:00:00",
                "6. Time Zone": "US/Eastern"
            },
            "Time Series (1min)": {
                "2024-01-15 16:00:00": {
                    "4. close": price
                }
            }
        })
        return mock_response

    @patch('tracker_app.views.requests.get')
    def test_stock_index_handles_api_error(self, mock_get):
        """Test that stock search handles API errors gracefully"""
        ticker_symbol = 'AAPL'

        # Mock API response without 'Meta Data' (simulating rate limit error)
        mock_response = Mock()
        mock_response.text = json.dumps({
            'Note': 'Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day.'
        })
        mock_get.return_value = mock_response

        # Call stock index
        url = reverse('stock-index')
        response = self.client.get(url, {'symbol': ticker_symbol, 'portfolio_id': self.portfolio.pk})

        # Verify returns to search form with error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/search_form.html')
        self.assertContains(response, "exceeded the request limit for the free equity lookup service")
        self.assertEqual(response.context['portfolio_id'], str(self.portfolio.pk))

    def _mock_api_response_by_symbol(self, prices_by_symbol):
        """Return a function that returns mock API responses based on symbol in URL."""
        def mock_response(url):
            response = Mock()
            for symbol, price in prices_by_symbol.items():
                if f'symbol={symbol}' in url:
                    response.text = json.dumps({
                        "Meta Data": {
                            "3. Last Refreshed": "2024-01-15 16:00:00",
                            "6. Time Zone": "US/Eastern"
                        },
                        "Time Series (1min)": {
                            "2024-01-15 16:00:00": {
                                "4. close": price
                            }
                        }
                    })
                    return response
            return response
        return mock_response
