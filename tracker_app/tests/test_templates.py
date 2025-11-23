import json
from decimal import Decimal

from django.test import TestCase, override_settings
from unittest.mock import patch, Mock

from tracker_app.models import Portfolio, Stock

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PortfolioTemplateTests(TestCase):

    def setUp(self):
        # For now, the test portfolio must be called 'Rainy Day Fund' because the root path pulls the seeded portfolio
        self.portfolio = Portfolio.objects.create(name="Rainy Day Fund")

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

    def test_root_url_displays_portfolio_template(self):
        response = self.client.get('/')

        # Verify receive successful response
        self.assertEqual(response.status_code, 200)

        # Verify display of page headers
        self.assertContains(response, 'Equity Portfolio')
        self.assertContains(response, 'Portfolio Name:')

        # Verify display of row labels
        row_labels = [
            'Symbol:',
            'Last Trade Time',
            'Last Trade Price',
            'Number of shares owned',
            'Market value of stake',
        ]

        for label in row_labels:
            # subTest will fail on individual row labels
            with self.subTest(label=label):
                self.assertContains(response, label)

    def test_root_url_displays_navigation_links(self):
        response = self.client.get('/')

        self.assertContains(response, f'<a href="/portfolio-refresh/{self.portfolio.pk}/">Refresh Prices</a>')
        self.assertContains(response, f'<a href="/search/?portfolio_id={self.portfolio.pk}">Search/Add Stocks</a>')
        self.assertContains(response, '<a href="/api/" target="_blank">Browsable API</a>')

    def test_root_url_displays_stock_data(self):
        response = self.client.get('/')

        for stock in Stock.objects.all():
            self.assertContains(response, stock.symbol)
            self.assertContains(response, f'{stock.shares_owned:.2f}')
            self.assertContains(response, f'{stock.last_trade_price:.2f}')

    def test_refresh_portfolio_prices_button_exists(self):
        """Test that the Refresh Prices button exists with correct link"""
        response = self.client.get('/')

        # Verify the refresh button is present with correct href
        self.assertContains(response, f'href="/portfolio-refresh/{self.portfolio.pk}/"')
        self.assertContains(response, 'Refresh Prices')

    @patch('tracker_app.views.requests.get')
    def test_refresh_portfolio_prices_user_flow(self, mock_get):
        """Test user flow: click refresh → redirect → see updated prices"""
        # Mock the API response that provides new price data
        new_prices_by_symbol = {'AAPL': '205.00', 'NVDA': '95.95'}
        mock_get.side_effect = self._mock_api_response(new_prices_by_symbol)

        # User clicks 'Refresh Prices' link
        response = self.client.get(f'/portfolio-refresh/{self.portfolio.pk}/')

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