from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^keyboard/',views.keyboard, name="keyboard"),
    url(r'^message',views.message, name="message"),
    url(r'^(?P<shortname>[a-z]+)/$', views.detail,name='detail'),
    url(r'^(?P<shortname>[a-z]+)/history/$',views.history,name='history'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>.*)/$',views.restaurant_detail,name='restaurant'),
]



