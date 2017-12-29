# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Portfolio(models.Model):

    name = models.CharField(max_length=200, unique=True, blank=False)  #not appropriate for a system with multiple users
    timestamp_last_updated = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name

    #limits portfolio size to 5 stocks and ensures that stocks are not duplicated
    def add_stock(self, new_stock):
        if self.stock_set.count() >= 5:
            raise Exception("You already have 5 stocks in this portfolio.")

        for old_stock in self.stock_set.all():
            if old_stock.id == new_stock.id:
                raise Exception("That stock is already in this portfolio.")

        self.stock_set.add(new_stock)


class Stock(models.Model):

    company_name = models.CharField(max_length=200, blank=True)
    symbol = models.CharField(max_length=20, unique=True, blank=False)
    timestamp_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    # last_trade_price = models.DecimalField(max_digits=19, decimal_places=3, blank=True, null=True) #defaults to None; preferred; using below for MVP
    last_trade_price = models.DecimalField(max_digits=19, decimal_places=3, default=Decimal('0.000'), blank=False) #defaults to 0.000 so buy_shares does not need to handle None type

    #below two should be combined in final version (e.g. update last_trade_price if last_updated == created OR last_updated > 5 seconds ago)
    last_trade_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp_last_updated = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    #below three are not appropriate for systems with multiple users or portfolios
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, blank=True, null=True)
    shares_owned = models.DecimalField(max_digits=19, decimal_places=3, default=Decimal('0.000'), blank=False)
    market_value = models.DecimalField(max_digits=19, decimal_places=3, default=Decimal('0.000'), blank=False)

    def __str__(self):
        return self.symbol


    #updates shares_owned and market_value; last_trade_price must be populated for this to work as expected; post-MVP, edit to handle last_trade_price as None type
    def buy_shares(self, number_of_shares):
        self.shares_owned = self.shares_owned + number_of_shares
        self.market_value = self.last_trade_price * self.shares_owned
        #do I need a manual save to database here?

    def remove_from_portfolio(self):
        self.portfolio = None
        #do I need a manual save to database here so portfolio stock_set also changed?





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
