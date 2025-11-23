from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from ..models import Portfolio, Stock


class PortfolioAPITests(APITestCase):
    """Test the Portfolio REST API endpoints"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")

    def test_api_root(self):
        """Test API root returns portfolio and stock links"""
        url = reverse('api:api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('portfolios', response.data)
        self.assertIn('stocks', response.data)

    def test_portfolio_list(self):
        """Test getting list of portfolios"""
        url = reverse('api:portfolio-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_portfolio_create(self):
        """Test creating a new portfolio via API"""
        url = reverse('api:portfolio-list')
        data = {'name': 'New Portfolio'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Portfolio.objects.count(), 2)
        self.assertEqual(Portfolio.objects.latest('id').name, 'New Portfolio')

    def test_portfolio_detail(self):
        """Test retrieving a specific portfolio"""
        url = reverse('api:portfolio-detail', args=[self.portfolio.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Portfolio')

    def test_portfolio_update(self):
        """Test updating a portfolio's name"""
        url = reverse('api:portfolio-detail', args=[self.portfolio.id])
        data = {'name': 'Updated Portfolio'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.name, 'Updated Portfolio')

    def test_portfolio_delete(self):
        """Test deleting a portfolio (should be protected if has stocks)"""
        url = reverse('api:portfolio-detail', args=[self.portfolio.id])
        response = self.client.delete(url)
        # Should succeed when no stocks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Portfolio.objects.count(), 0)


class StockAPITests(APITestCase):
    """Test the Stock REST API endpoints"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")
        self.stock = Stock.objects.create(
            symbol="AAPL",
            last_trade_price=Decimal("150.000"),
            portfolio=self.portfolio,
            shares_owned=Decimal("10.000")
        )

    def test_stock_list(self):
        """Test getting list of stocks"""
        url = reverse('api:stock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_stock_create(self):
        """Test creating a new stock via API"""
        url = reverse('api:stock-list')
        data = {
            'symbol': 'GOOGL',
            'last_trade_price': '2800.500',
            'shares_owned': '5.000'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 2)

    def test_stock_detail(self):
        """Test retrieving a specific stock"""
        url = reverse('api:stock-detail', args=[self.stock.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'AAPL')

    def test_stock_update(self):
        """Test updating a stock"""
        url = reverse('api:stock-detail', args=[self.stock.id])
        data = {
            'symbol': 'AAPL',
            'last_trade_price': '155.000',
            'shares_owned': '15.000'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.last_trade_price, Decimal("155.000"))

    def test_stock_delete(self):
        """Test deleting a stock"""
        url = reverse('api:stock-detail', args=[self.stock.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Stock.objects.count(), 0)
