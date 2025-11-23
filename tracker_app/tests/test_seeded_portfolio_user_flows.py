from django.test import TestCase, override_settings

from tracker_app.models import Portfolio, Stock

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SeededPortfolioTemplateTests(TestCase):
    """Tests for the root URL which displays the seeded 'Rainy Day Fund' portfolio."""

    fixtures = ['initdata.json']

    def setUp(self):
        self.portfolio = Portfolio.objects.get(name="Rainy Day Fund")

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

        self.assertContains(response, f'<a href="/portfolios/{self.portfolio.pk}/refresh/">Refresh Prices</a>')
        self.assertContains(response, f'<a href="/search/?portfolio_id={self.portfolio.pk}">Search/Add Stocks</a>')
        self.assertContains(response, '<a href="/api/" target="_blank">Browsable API</a>')

    def test_root_url_displays_stock_data(self):
        response = self.client.get('/')

        for stock in Stock.objects.all():
            self.assertContains(response, stock.symbol)
            self.assertContains(response, f'{stock.shares_owned:.2f}')
            self.assertContains(response, f'{stock.last_trade_price:.2f}')
