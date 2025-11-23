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

    re_path(r'^api/', include('tracker_app.urls')),
    re_path(r'^admin/', admin.site.urls),

    # updated stock data by ticker symbol
    re_path(r'^search/$', views.render_search_form, name='search-form'),
    re_path(r'^stocks/$', views.stock_index, name='stock-index'),

    # stock details for each stock in a given portfolio
    re_path(r'^portfolios/(?P<pk>[0-9]+)/stocks/(?P<symbol>.+)/$', views.stock_detail_for_portfolio, name='portfolio-stock-detail'),

    # remove stock from portfolio
    re_path(r'^stockDELETE/(?P<pk>[0-9]+)/$', views.delete_stock, name='delete-stock'),

    # refresh price data in a given portfolio
    re_path(r'^portfolio-refresh/(?P<pk>[0-9]+)/$', views.refresh_portfolio, name='refresh-portfolio'),

    # dead code
    re_path(r'^stocksOLD/$', views.stockOLD_index, name='stockOLD-index'),
    re_path(r'^stocksOLD/(?P<pk>[0-9]+)/$', views.stockOLD_detail, name='stockOLD-detail'),

    # At root path, display the seeded portfolio
    re_path(r'^$', views.view_seeded_portfolio, name='view-seeded-portfolio'),

]
