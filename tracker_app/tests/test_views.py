from django.test import TestCase, override_settings
from django.urls import reverse
from decimal import Decimal

from ..models import Portfolio, Stock


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FrontendViewTests(TestCase):
    """Test frontend views"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Chris")
        self.stock = Stock.objects.create(
            symbol="AAPL",
            last_trade_price=Decimal("150.000"),
            portfolio=self.portfolio,
            shares_owned=Decimal("10.000")
        )

    def test_load_portfolio_chris(self):
        """Test loading Chris' portfolio page"""
        url = reverse('load-portfolio-chris')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chris')
        self.assertContains(response, 'AAPL')

    def test_render_search_form(self):
        """Test rendering the stock search form"""
        url = reverse('search-form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_stock_view(self):
        """Test deleting a stock through the frontend"""
        url = reverse('delete-stock', args=[self.stock.pk])
        response = self.client.post(url)

        # Should redirect
        self.assertEqual(response.status_code, 302)

        # Stock should be deleted
        self.assertEqual(Stock.objects.count(), 0)
