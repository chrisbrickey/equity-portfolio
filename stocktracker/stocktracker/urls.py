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
from django.conf.urls import url, include
from tracker_app import views   #for frontend only

urlpatterns = [

    url(r'^api/', include('tracker_app.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^search/$', views.render_search_form, name='search-form'),
    url(r'^stocks/$', views.stock_index, name='stock-index'),
    url(r'^stocks/(?P<symbol>.+)/$', views.stock_detail, name='stock-detail'),

    url(r'^stocksOLD/$', views.stockOLD_index, name='stockOLD-index'),
    url(r'^stocksOLD/(?P<pk>[0-9]+)/$', views.stockOLD_detail, name='stockOLD-detail'),

    # implement below for system with multiple portfolios
    # url(r'^portfolios/$', views.portfolio_index, name='index'),
    # url(r'^portfolios/(?P<pk>[0-9]+)/$', views.portfolio_detail, name='detail'),

    url(r'^$', views.load_portfolio_horace, name='horace'),  #the top level shows Horace's portfolio detail

]
