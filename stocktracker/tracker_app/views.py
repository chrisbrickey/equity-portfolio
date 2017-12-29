# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import generics, renderers
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import Portfolio, Stock
from .serializers import PortfolioSerializer, StockSerializer

# for API Root
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import requests
import json


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
def portfolio_horace(request):
    horace_portfolio_set = Portfolio.objects.filter(name="Horace") #pulls first 100 stocks based on symbol ABC order
    horace_stock_queryset = horace_portfolio_set[0].stock_set.all()

    if horace_portfolio_set.exists():
        context = {'portfolio': horace_portfolio_set[0], 'stock_set': horace_stock_queryset}
        return render(request, 'portfolios/horace.html', context)
    else:
        raise Http404("We can't find Horace's portfolio in our database.")


def render_search_form(request):
    return render(request, 'stocks/search_form.html')


def stockA_index(request):
    symbol = request.GET.get('symbol', None)
    api_call = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={0}&interval=1min&apikey=Z8GRK4D67R58DDGC".format(symbol)
    response = requests.get(api_call)
    stock_text = response.text
    stock_dict = json.loads(stock_text)

    meta_data = stock_dict['Meta Data']
    time_zone = meta_data['6. Time Zone']
    latest_date_time = meta_data['3. Last Refreshed']

    closing_price = stock_dict['Time Series (1min)'][latest_date_time]['4. close']

    context = {'symbol': symbol,
               'latest_date_time': latest_date_time,
               'closing_price': closing_price,
               'time_zone': time_zone}

    return render(request, 'stocks/search_result.html', context)


@csrf_exempt
def stockA_detail(request, symbol):

    if request.method == 'DELETE':
        stock_to_delete = Stock.objects.get(symbol=symbol)
        stock_to_delete.remove_from_portfolio()
        stock_to_delete.delete()

        context = {'portfolio': horace_portfolio, 'stock_set': horace_stock_queryset}
        return render(request, 'portfolios/horace.html', context)

    elif request.method == 'POST':
        last_trade_price = request.POST.get('last_trade_price', None)
        last_trade_time = request.POST.get('last_trade_time', None)
        n_shares = request.POST.get('n_shares', None)
        n_shares = str(n_shares)
        horace_portfolio = Portfolio.objects.get(name="Horace")

        new_stock = Stock(symbol=symbol, last_trade_time=last_trade_time, last_trade_price=last_trade_price)

        try:
            new_stock.save()
        except:
            render(request, 'stocks/search_form.html', { 'error_message' : "This stock is already in the portfolio. Please choose another."})

        try:
            horace_portfolio.add_stock(new_stock)
        except:
            render(request, 'stocks/search_form.html', { 'error_message' : "This stock is already in the portfolio or the portfolio is full."})

        new_stock.buy_shares(n_shares)
        horace_stock_queryset = horace_portfolio.stock_set.all()
        context = {'portfolio': horace_portfolio, 'stock_set': horace_stock_queryset}
        return render(request, 'portfolios/horace.html', context)

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



# IMPLEMENT BELOW FOR SYSTEM WITH MULTIPLE PORTFOLIOS
# def portfolio_index(request):
#     portfolio_list = Portfolio.objects.order_by('name')[:100] #pulls first 100 portfolios based on name ABC order
#     context = {'portfolio_list': portfolio_list}
#     return render(request, 'portfolios/index.html', context)

# def portfolio_detail(request, pk):
#     try:
#         portfolio = Portfolio.objects.get(pk=pk)
#         # portfolio = Portfolio.objects.get(name=portfolio_name)
#     except Portfolio.DoesNotExist:
#         raise Http404("That portfolio does not exist in our database.")
#
#     context = {'portfolio': portfolio}
#     return render(request, 'portfolios/detail.html', context)
