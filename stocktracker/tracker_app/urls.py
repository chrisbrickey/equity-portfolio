#
from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^stocks/$', views.StockList.as_view()),
    url(r'^stocks/(?P<pk>[0-9]+)/$', views.StockDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
