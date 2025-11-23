"""stocktracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import re_path, include
from tracker_app import views   #for frontend only

urlpatterns = [

    # ADMIN ROUTES
    re_path(r'^api/', include('tracker_app.urls')),
    re_path(r'^admin/', admin.site.urls),

    # STOCK ROUTES

    # renders empty search form
    re_path(r'^search/$', views.render_search_form, name='search-form'),

    # fetch current price (and metadata) by ticker symbol in query parameter
    re_path(r'^stocks/$', views.stock_index, name='stock-index'),

    # PORTFOLIO ROUTES

    # detail view of a portfolio
    re_path(r'^portfolios/(?P<pk>[0-9]+)/$', views.view_portfolio, name='view-portfolio'),

    # refresh price data of all stocks in a portfolio
    re_path(r'^portfolios/(?P<pk>[0-9]+)/refresh/$', views.refresh_portfolio, name='refresh-portfolio'),

    # update shares of stock in portfolio (must come before symbol catch-all)
    re_path(r'^portfolios/(?P<pk>[0-9]+)/stocks/(?P<stock_pk>[0-9]+)/update/$', views.update_stock_shares, name='stock-update'),

    # remove stock from portfolio (must come before symbol catch-all)
    re_path(r'^portfolios/(?P<pk>[0-9]+)/stocks/(?P<stock_pk>[0-9]+)/delete/$', views.delete_stock, name='delete-stock'),

    # display all stocks in a given portfolio (catch-all for symbol, must be last)
    re_path(r'^portfolios/(?P<pk>[0-9]+)/stocks/(?P<symbol>.+)/$', views.stock_detail_for_portfolio, name='portfolio-stock-detail'),

    # ROOT ROUTE
    # Display seeded portfolio
    re_path(r'^$', views.view_seeded_portfolio, name='view-seeded-portfolio'),

]
