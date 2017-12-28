# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from .models import Stock
from .serializers import StockSerializer

from rest_framework import generics

class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
