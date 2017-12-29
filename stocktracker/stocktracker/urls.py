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

    # implement below for system with multiple portfolios
    # url(r'^portfolios/$', views.portfolio_index, name='index'),
    # url(r'^portfolios/(?P<pk>[0-9]+)/$', views.portfolio_detail, name='detail'),

    url(r'^stocks/$', views.stock_index, name='index'),
    url(r'^stocks/(?P<pk>[0-9]+)/$', views.stock_detail, name='detail'),
    url(r'^stocks/(?P<stock_sym>.+)/$', views.add_stock, name='add-stock'),
    
    url(r'^retrieve/(?P<stock_sym>.+)/$', views.retrieve_stock_detail, name='manual-detail'),

    url(r'^search/$', views.render_search_form, name='search-form'),
    url(r'^alpha/$', views.search_stock, name='search-stock'),
    # url(r'^alpha/(?P<symbol>.+)/$', views.search_stock, name='search-stock'),

    url(r'^$', views.portfolio_horace, name='horace'),  #the top level shows Horace's portfolio detail

]
