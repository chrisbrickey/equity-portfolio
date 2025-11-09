from rest_framework import serializers
from .models import Portfolio, Stock, LANGUAGE_CHOICES, STYLE_CHOICES


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    stock_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Portfolio
        fields = ('url',
                  'id',
                  'name',
                  'stock_set',
                  'timestamp_created')
        extra_kwargs = {
            'url': {'view_name': 'api:portfolio-detail'},
        }


class StockSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stock
        fields = ('url',
                  'id',
                  'symbol',
                  'last_trade_price',
                  'portfolio',
                  'shares_owned',
                  'timestamp_created',
                  'last_trade_time')
        extra_kwargs = {
            'url': {'view_name': 'api:stock-detail'},
            'portfolio': {'view_name': 'api:portfolio-detail'},
        }
