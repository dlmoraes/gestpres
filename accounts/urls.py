# coding=utf-8

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil/avatar/(?P<pk>[\w_-]+)/$', views.alterar_avatar, name="alterar_avatar"),
 ]