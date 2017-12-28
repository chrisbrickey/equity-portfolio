# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Stock(models.Model):

    company_name = models.CharField(max_length=200, blank=True)
    symbol = models.CharField(max_length=20, unique=True, blank=False)
    last_trade_price = models.DecimalField(max_digits=19, decimal_places=3, blank=True, null=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    #placing shares owned within Stock model is not appropriate for multiple users/portfolios
    shares_owned = models.DecimalField(max_digits=19, decimal_places=3, default=Decimal('0.000'), blank=False)

    #below two should be combined in final version (e.g. update last_trade_price if last_updated == created OR last_updated > 5 seconds ago)
    last_trade_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp_last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # field to display on Django admin and whenever using string representation of entire object; must be unique
    def __str__(self):
        return self.symbol


# implement below model for multiple users/portfolios
# class Follow(models.Model):
#
#     portfolio_id = models.ForeignKey(Portfolio, on_delete=models.PROTECT)
#     stock_id = models.ForeignKey(Stock, on_delete=models.PROTECT)
#     shares_owned = models.DecimalField(max_digits=19, decimal_places=3, default=Decimal('0.000'), blank=False)
#     timestamp_last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)
#
#     def __str__(self):
#         return self.id


# implement below model for multiple users/portfolios
# class Portfolio(models.Model):
#
#     timestamp_last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)
#
#     def __str__(self):
#         return self.id
