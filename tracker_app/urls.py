#Browsable API URLs
from django.urls import re_path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = format_suffix_patterns([

    re_path(r'^$', views.api_root, name='api-root'),

    re_path(r'^portfolios/$', views.PortfolioList.as_view(), name='portfolio-list'),
    re_path(r'^portfolios/(?P<pk>[0-9]+)/$', views.PortfolioDetail.as_view(), name='portfolio-detail'),

    re_path(r'^stocks/$', views.StockList.as_view(), name='stock-list'),
    re_path(r'^stocks/(?P<pk>[0-9]+)/$', views.StockDetail.as_view(), name='stock-detail'),


])
