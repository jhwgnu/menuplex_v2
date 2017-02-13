from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<shortname>[a-z]+)/$', views.detail,name='detail'),
    url(r'^(?P<shortname>[a-z]+)/history/$',views.history,name='history'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/$',views.restaurant_detail,name='restaurant'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/comments/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/comments/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]



