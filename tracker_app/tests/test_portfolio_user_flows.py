import json
from decimal import Decimal

from django.test import TestCase, override_settings
from unittest.mock import patch, Mock

from tracker_app.models import Portfolio, Stock

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PortfolioUserFlowTests(TestCase):
    """Tests for portfolio functionality that are independent of the seeded portfolio."""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")

        Stock.objects.create(
            symbol='AAPL',
            portfolio=self.portfolio,
            shares_owned=Decimal('5.000'),
            last_trade_price=Decimal('200.01'),
        )
        Stock.objects.create(
            symbol='NVDA',
            portfolio=self.portfolio,
            shares_owned=Decimal('7.000'),
            last_trade_price=Decimal('100.00'),
        )

    def test_refresh_portfolio_prices_button_exists(self):
        """Test that the Refresh Prices button exists with correct link"""
        response = self.client.get(f'/portfolios/{self.portfolio.pk}/')

        # Verify the refresh button is present with correct href
        self.assertContains(response, f'href="/portfolios/{self.portfolio.pk}/refresh/"')
        self.assertContains(response, 'Refresh Prices')

    @patch('tracker_app.views.requests.get')
    def test_refresh_portfolio_prices_user_flow(self, mock_get):
        """Test user flow: click refresh → redirect → see updated prices"""
        # Mock the API response that provides new price data
        new_prices_by_symbol = {'AAPL': '205.00', 'NVDA': '95.95'}
        mock_get.side_effect = self._mock_api_response(new_prices_by_symbol)

        # User clicks 'Refresh Prices' link
        response = self.client.get(f'/portfolios/{self.portfolio.pk}/refresh/')

        # Verify that user is redirected back to portfolio view
        self.assertRedirects(response, f'/portfolios/{self.portfolio.pk}/')

        # Verify that user sees updated prices on the page
        response = self.client.get(f'/portfolios/{self.portfolio.pk}/')
        for price in new_prices_by_symbol.values():
            self.assertContains(response, price)

    def _mock_api_response(self, prices_by_symbol):
        """Return a function that mocks API responses based on stock symbol in URL."""
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
