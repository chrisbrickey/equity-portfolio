# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Portfolio, Stock

admin.site.register(Portfolio)
admin.site.register(Stock)
