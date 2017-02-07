from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<school_id>\d+)/$', views.detail,name='detail'),
    url(r'^(?P<school_id>\d+)/(?P<restaurant_id>\d+)/$',views.restaurant_detail,name='restaurant'),
]