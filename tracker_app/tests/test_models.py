from django.test import TestCase
from decimal import Decimal

from ..models import Portfolio, Stock


class PortfolioModelTests(TestCase):
    """Test the Portfolio model and its business logic"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")

    def test_portfolio_creation(self):
        """Test that a portfolio can be created"""
        self.assertEqual(self.portfolio.name, "Test Portfolio")
        self.assertIsNotNone(self.portfolio.timestamp_created)

    def test_portfolio_str_representation(self):
        """Test the string representation of a portfolio"""
        self.assertEqual(str(self.portfolio), "Test Portfolio")

    def test_add_stock_to_portfolio(self):
        """Test adding a stock to a portfolio"""
        stock = Stock.objects.create(symbol="AAPL")
        self.portfolio.add_stock(stock)
        self.assertEqual(self.portfolio.stock_set.count(), 1)
        self.assertIn(stock, self.portfolio.stock_set.all())

    def test_portfolio_limit_five_stocks(self):
        """Test that portfolio cannot exceed 5 stocks"""
        # Add 5 stocks
        for i in range(5):
            stock = Stock.objects.create(symbol=f"STOCK{i}")
            self.portfolio.add_stock(stock)

        self.assertEqual(self.portfolio.stock_set.count(), 5)

        # Try to add 6th stock - should raise exception
        sixth_stock = Stock.objects.create(symbol="SIXTH")
        with self.assertRaises(Exception) as context:
            self.portfolio.add_stock(sixth_stock)

        self.assertIn("already have 5 stocks", str(context.exception))

    def test_prevent_duplicate_stocks_in_portfolio(self):
        """Test that the same stock cannot be added twice"""
        stock = Stock.objects.create(symbol="AAPL")
        self.portfolio.add_stock(stock)

        # Try to add same stock again
        with self.assertRaises(Exception) as context:
            self.portfolio.add_stock(stock)

        self.assertIn("already in this portfolio", str(context.exception))


class StockModelTests(TestCase):
    """Test the Stock model and its business logic"""

    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")
        self.stock = Stock.objects.create(
            symbol="AAPL",
            last_trade_price=Decimal("150.000")
        )

    def test_stock_creation(self):
        """Test that a stock can be created"""
        self.assertEqual(self.stock.symbol, "AAPL")
        self.assertEqual(self.stock.last_trade_price, Decimal("150.000"))
        self.assertIsNotNone(self.stock.timestamp_created)

    def test_stock_str_representation(self):
        """Test the string representation of a stock"""
        self.assertEqual(str(self.stock), "AAPL")

    def test_buy_shares(self):
        """Test buying shares of a stock"""
        self.stock.buy_shares(10)
        self.assertEqual(self.stock.shares_owned, Decimal("10.000"))

        # Buy more shares
        self.stock.buy_shares(5.5)
        self.assertEqual(self.stock.shares_owned, Decimal("15.500"))

    def test_buy_shares_with_empty_string(self):
        """Test buy_shares with empty string defaults to 0"""
        self.stock.buy_shares("")
        self.assertEqual(self.stock.shares_owned, Decimal("0.000"))

    def test_remove_from_portfolio(self):
        """Test removing a stock from its portfolio"""
        self.stock.portfolio = self.portfolio
        self.stock.shares_owned = Decimal("10.000")
        self.stock.save()

        self.stock.remove_from_portfolio()

        self.assertIsNone(self.stock.portfolio)
        self.assertEqual(self.stock.shares_owned, Decimal("0.000"))
