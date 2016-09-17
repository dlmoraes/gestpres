#coding=utf-8
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^empresa/$', views.empresas, name="empresas"),
    url(r'^regional/$', views.regionais, name="regionais"),
    url(r'^baseregional/$', views.basesregionais, name="basesregionais"),
    url(r'^pex/$', views.tipos, name="tipos"),
    url(r'^pex/pas/$', views.pas, name="pas"),
    url(r'^infraestrutura/link/$', views.links, name="links"),
    url(r'^agencias/$', views.agencias, name="agencias"),
    url(r'^agencias/detalhes/(?P<pk>[\w_-]+)/$', views.agencia_detalhes, name="agencia_detalhes"),
]