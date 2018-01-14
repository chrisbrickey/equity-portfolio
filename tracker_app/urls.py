#Browsable API URLs
from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([

    url(r'^$', views.api_root),

    url(r'^portfolios/$', views.PortfolioList.as_view(), name='portfolio-list'),
    url(r'^portfolios/(?P<pk>[0-9]+)/$', views.PortfolioDetail.as_view(), name='portfolio-detail'),

    url(r'^stocks/$', views.StockList.as_view(), name='stock-list'),
    url(r'^stocks/(?P<pk>[0-9]+)/$', views.StockDetail.as_view(), name='stock-detail'),


])
