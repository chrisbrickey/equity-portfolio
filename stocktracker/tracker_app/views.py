# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import generics, renderers
from django.template import loader

from .models import Portfolio, Stock
from .serializers import PortfolioSerializer, StockSerializer

# for API Root
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import requests


# BROWSABLE API
class PortfolioList(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class PortfolioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'portfolios': reverse('portfolio-list', request=request, format=format),
        'stocks': reverse('stock-list', request=request, format=format)
    })



# FRONTEND
def stock_index(request):
    stock_list = Stock.objects.order_by('symbol')[:100] #pulls first 100 stocks based on symbol ABC order
    context = {'stock_list': stock_list}

    #arguments required for render: input request, path to template you want to render, context=variables you need to pass to template
    return render(request, 'stocks/index.html', context)


def stock_detail(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
        # stock = Stock.objects.get(symbol=stock_symbol)
    except Stock.DoesNotExist:
        raise Http404("That stock does not exist in our database.")

    context = {'stock': stock}
    return render(request, 'stocks/detail.html', context)



# EXPERIMENTS
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
