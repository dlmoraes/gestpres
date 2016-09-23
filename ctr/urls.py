#coding=utf-8
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^treinamento/$', views.treinamentos, name="treinamentos"),
    url(r'^treinamento/inicial/add/$', views.treinamento_inicial_add, name="treinamento_inicial_add"),
    url(r'^treinamento/inicial/update/(?P<pk>\d+)/$', views.treinamento_inicial_update, name='treinamento_inicial_update'),
    url(r'^treinamento/rotina/add/$', views.treinamento_rotina_add, name="treinamento_rotina_add"),
    url(r'^treinamento/rotina/update/(?P<pk>\d+)/$', views.treinamento_rotina_update,
        name='treinamento_rotina_update'),
    url(r'^matriculados/(?P<treinamento_pk>\d+)/$', views.matriculas_treinamento, name='avaliar_treinamento'),
    url(r'^matriculado/(?P<pk>\d+)/treinamento/(?P<treinamento_pk>\d+)/$', views.avaliar_matriculado, name='avaliar_matriculado'),
    url(r'^pesquisa_matricula/$', views.pesquisa_matricula, name='pesquisa_matricula'),
]