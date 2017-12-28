from rest_framework import serializers
from .models import Portfolio, Stock, LANGUAGE_CHOICES, STYLE_CHOICES


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Portfolio
        fields = ('url',        #we get this from HyperlinkedIdentityField
                  'id',
                  'name',
                  'timestamp_created',
                  'timestamp_last_updated')
        # restrict fields after determining what is required or add conditionals here to restrict data sent to frontend based on query string filters


#previously used ModelSerializer as inheriting class which uses default versions of create() and update()
class StockSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stock
        fields = ('url',        #we get this from HyperlinkedIdentityField
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
