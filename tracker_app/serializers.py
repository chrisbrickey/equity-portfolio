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
