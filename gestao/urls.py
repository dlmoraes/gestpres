#coding=utf-8
from copy import name

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.static import serve as serve_static

from core import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^controle_agencias/', include('cag.urls', namespace='cag')),
    url(r'^controle_pessoas/', include('cat.urls', namespace='cat')),
    url(r'^conta/', include('accounts.urls', namespace='accounts')),
    url(r'^controle_treinamentos/', include('ctr.urls', namespace='ctr')),
    url(r'^admin/', admin.site.urls),
    url(r'^entrar/$', login, {'template_name' : 'login.html'}, name='login'),
    url(r'^sair/$', logout, {'next_page' : '/'}, name='logout'),    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]