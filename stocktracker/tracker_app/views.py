# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import generics, renderers

from .models import Stock
from .serializers import StockSerializer

# for API Root
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import requests


class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'stocks': reverse('stock-list', request=request, format=format)
    })




#playing around with frontend
def index(request):
    stock_list = Stock.objects.order_by('symbol')[:100] #pulls first 100 stocks based on symbol ABC order
    stock_string = ', '.join([stock.symbol for stock in stock_list])
    response = "Here is a list of all stocks in our database:\n" + stock_string
    return HttpResponse(response)

def custom_method_test(request, query_string):
    response = "custom method received: {0}"
    return HttpResponse(response.format(query_string))

def retrieve_stock_detail(request, stock_sym):
    try:
        s = Stock.objects.get(symbol=stock_sym)
    except Stock.DoesNotExist:
        raise Http404("Stock does not exist")

    response = "Symbol: {0}, Name: {1}, Price: {2}, Shares Owned: {3}"
    return HttpResponse(response.format(s.symbol, s.company_name, s.last_trade_price, s.shares_owned))

def alpha_vantage_demo(request, time_frequency): #5min
    api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval={0}&apikey=Z8GRK4D67R58DDGC".format(time_frequency)
    response = requests.get(api_call)
    return HttpResponse(response.text)
    # return HttpResponse(response.json())
