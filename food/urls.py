from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<school_id>\d+)/$', views.detail,name='detail'),
    url(r'^(?P<school_id>\d+)/(?P<restaurant_name>.*)/$',views.restaurant_detail,name='restaurant'),
]