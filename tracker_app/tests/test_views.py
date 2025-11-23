from django.test import TestCase, override_settings
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch, Mock
import json

from ..models import Portfolio, Stock


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ViewErrorTests(TestCase):
    """Tests for view error handling (404s, validation errors, etc.)"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")

    def test_refresh_portfolio_returns_404_when_not_found(self):
        """Test that refresh returns 404 for non-existent portfolio"""
        non_existent_portfolio = 99999
        url = reverse('refresh-portfolio', kwargs={'pk': non_existent_portfolio})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_stock_detail_returns_404_when_portfolio_not_found(self):
        """Test that stock detail returns 404 for non-existent portfolio"""
        non_existent_portfolio = 99999
        url = f'/portfolios/{non_existent_portfolio}/stocks/AAPL/'
        response = self.client.post(url, {
            'last_trade_price': '150.00',
            'last_trade_time': '2024-01-15T16:00:00-05:00',
            'n_shares': '10',
        })

        self.assertEqual(response.status_code, 404)

    def test_stock_detail_error_when_duplicate_symbol(self):
        """Test that adding a stock with duplicate symbol shows error message"""
        # Create existing stock with symbol AAPL
        Stock.objects.create(
            symbol='AAPL',
            portfolio=self.portfolio,
            shares_owned=Decimal('10.000'),
            last_trade_price=Decimal('150.00'),
        )

        # Try to add another stock with same symbol
        url = f'/portfolios/{self.portfolio.pk}/stocks/AAPL/'
        response = self.client.post(url, {
            'last_trade_price': '155.00',
            'last_trade_time': '2024-01-15T16:00:00-05:00',
            'n_shares': '5',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/search_form.html')
        self.assertContains(response, "This stock is already in the portfolio. Please choose another.")
        self.assertEqual(int(response.context['portfolio_id']), self.portfolio.pk)

    def test_stock_detail_error_when_portfolio_full(self):
        """Test that adding a stock to a full portfolio (5 stocks) shows error message"""
        # Create 5 stocks in portfolio
        for i in range(5):
            Stock.objects.create(
                symbol=f'STK{i}',
                portfolio=self.portfolio,
                shares_owned=Decimal('10.000'),
                last_trade_price=Decimal('100.00'),
            )

        # Try to add 6th stock
        url = f'/portfolios/{self.portfolio.pk}/stocks/NEWSTOCK/'
        response = self.client.post(url, {
            'last_trade_price': '50.00',
            'last_trade_time': '2024-01-15T16:00:00-05:00',
            'n_shares': '10',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/search_form.html')
        self.assertContains(response, "This stock is already in the portfolio or the portfolio is full.")
        self.assertEqual(int(response.context['portfolio_id']), self.portfolio.pk)

    def test_stock_detail_error_when_stock_already_in_portfolio(self):
        """Test that adding a stock that already exists in portfolio shows error message"""
        # Create a stock that's already in the portfolio
        existing_stock = Stock.objects.create(
            symbol='GOOGL',
            portfolio=self.portfolio,
            shares_owned=Decimal('5.000'),
            last_trade_price=Decimal('140.00'),
        )

        # Create another stock with different symbol (not in any portfolio yet)
        new_stock = Stock.objects.create(
            symbol='MSFT',
            portfolio=None,
            shares_owned=Decimal('0.000'),
            last_trade_price=Decimal('300.00'),
        )

        # Add the new stock to portfolio first
        self.portfolio.add_stock(new_stock)

        # Now try to add it again via the view - this will fail at add_stock
        # because the stock is already in the portfolio
        # Note: This test actually triggers the duplicate symbol error first
        # because Stock has unique=True on symbol field
        url = f'/portfolios/{self.portfolio.pk}/stocks/MSFT/'
        response = self.client.post(url, {
            'last_trade_price': '305.00',
            'last_trade_time': '2024-01-15T16:00:00-05:00',
            'n_shares': '10',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/search_form.html')
        # Will show duplicate symbol error since symbol is unique
        self.assertContains(response, "This stock is already in the portfolio. Please choose another.")
        self.assertEqual(int(response.context['portfolio_id']), self.portfolio.pk)

    @patch('tracker_app.views.requests.get')
    def test_refresh_portfolio_handles_api_error(self, mock_get):
        """Test that refresh portfolio handles API errors gracefully"""
        # Create a stock in the portfolio
        Stock.objects.create(
            symbol='AAPL',
            portfolio=self.portfolio,
            shares_owned=Decimal('10.000'),
            last_trade_price=Decimal('150.00'),
        )

        # Mock API response without 'Meta Data' (simulating rate limit error)
        mock_response = Mock()
        mock_response.text = json.dumps({
            'Note': 'Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day.'
        })
        mock_get.return_value = mock_response

        # Call refresh portfolio
        url = reverse('refresh-portfolio', kwargs={'pk': self.portfolio.pk})
        response = self.client.get(url)

        # Verify stays on portfolio page with error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolios/detail.html')
        self.assertContains(response, "exceeded the request limit for the free equity lookup service")
        self.assertEqual(response.context['portfolio'].pk, self.portfolio.pk)
