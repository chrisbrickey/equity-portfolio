from django.test import TestCase, override_settings

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PortfolioTemplateTests(TestCase):
    fixtures = ['initdata.json']

    def test_root_url_displays_portfolio_template(self):
        response = self.client.get('/')

        # Receive successful response
        self.assertEqual(response.status_code, 200)

        # Display page headers
        self.assertContains(response, 'Equity Portfolio')
        self.assertContains(response, 'Portfolio Name:')

        # Display row labels
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

        # TODO: update URL config and template to remove all caps from the update button
        self.assertContains(response, '<a href="/portfolioUPDATE/">Update Trade Prices</a>')
        self.assertContains(response, '<a href="/search/">Search/Add Stocks</a>')
        self.assertContains(response, '<a href="/">Your Portfolio</a>')
        self.assertContains(response, '<a href="/api/" target="_blank">Browsable API</a>')

    def test_root_url_displays_seeded_stock_data(self):
        from tracker_app.models import Stock
        response = self.client.get('/')

        # for all stocks in the seeded portfolio (see fixture)...
        for stock in Stock.objects.all():
            self.assertContains(response, stock.symbol)
            self.assertContains(response, f'{stock.shares_owned:.2f}')
            self.assertContains(response, f'{stock.last_trade_price:.2f}')
