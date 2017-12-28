from rest_framework import serializers
from .models import Stock, LANGUAGE_CHOICES, STYLE_CHOICES

class StockSerializer(serializers.ModelSerializer):
    #ModelSerializer classes use default versions of create() and update()

    class Meta:
        model = Stock
        fields = ('id',
                  'symbol',
                  'company_name',
                  'last_trade_price',
                  'shares_owned',
                  'timestamp_created',
                  'timestamp_last_updated',
                  'last_trade_time')
        # restrict fields after determining what is required or add conditionals here to restrict data sent to frontend based on query string filters
