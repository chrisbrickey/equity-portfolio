from rest_framework import serializers
from .models import Portfolio, Stock, LANGUAGE_CHOICES, STYLE_CHOICES

# ModelSerializer uses default versions of create() and update()
# decided against HyperlinkedModelSerializer due to increased complexity when creating new objects with relationships
class PortfolioSerializer(serializers.ModelSerializer):
    stock_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Portfolio
        fields = ('url',
                  'id',
                  'name',
                  'stock_set',
                  'timestamp_created',
                  'timestamp_last_updated')
        # restrict fields after determining what is required or add conditionals here to restrict data sent to frontend based on query string filters



class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('url',
                  'id',
                  'symbol',
                  'company_name',
                  'last_trade_price',
                  'portfolio',
                  'shares_owned',
                  'timestamp_created',
                  'timestamp_last_updated',
                  'last_trade_time')
        # restrict fields after determining what is required or add conditionals here to restrict data sent to frontend based on query string filters
