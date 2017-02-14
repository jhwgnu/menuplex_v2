from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^keyboard/',views.keyboard, name="keyboard"),
    url(r'^message',views.message, name="message"),
    url(r'^(?P<shortname>[a-z]+)/$', views.detail,name='detail'),
    url(r'^(?P<shortname>[a-z]+)/history/$',views.history,name='history'),
    url(r'^(?P<shortname>[a-z]+)/bool/$',views.bool,name='bool'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/$',views.restaurant_detail,name='restaurant'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/comments/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/comments/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/(?P<meal_pk>\d+)/mealcomment/$', views.meal_comment, name='meal_comment'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/(?P<meal_pk>\d+)/mealcomment/(?P<pk>\d+)/delete/$', views.meal_comment_delete, name='meal_comment_delete'),
    url(r'^(?P<shortname>[a-z]+)/(?P<restaurant_name>[^/]*)/(?P<meal_pk>\d+)/mealcomment/(?P<pk>\d+)/edit/$', views.meal_comment_edit, name='meal_comment_edit'),
]
