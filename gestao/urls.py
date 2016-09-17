#coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from core import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^controle_agencias/', include('cag.urls', namespace='cag')),
    url(r'^admin/', admin.site.urls),
    url(r'^entrar/$', login, {'template_name' : 'login.html'}, name='login'),
    url(r'^sair/$', logout, {'next_page' : '/'}, name='logout'),    
]
