from django.conf.urls import url
from . import views

urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^look$', views.look),
    url(r'^canvas$', views.canvas),
    url(r'^create_collab$', views.create_collab),
    url(r'^landing$', views.landing),
    url(r'^collab/(?P<collab_id>\d+)$', views.view_collab),
    url(r'^canvas/(?P<collab_id>\d+)$', views.canvas),
    url(r'^user/(?P<user_id>\d+)$', views.view_user),

]