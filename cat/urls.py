#coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cargo/$', views.cargos, name="cargos"),
    # url(r'^cargo/add/$', views.add_cargo, name="add_cargo"),
    url(r'^pessoa/$', views.pessoas, name="pessoas"),
    url(r'^atendente/$', views.atendentes, name="atendentes"),
]