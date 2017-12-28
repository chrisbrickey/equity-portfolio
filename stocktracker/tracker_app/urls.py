#
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^stocks/$', views.StockList.as_view()),
    url(r'^stocks/(?P<pk>[0-9]+)/$', views.StockDetail.as_view()),
]
