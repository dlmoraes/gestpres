#coding=utf-8
from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display = ['user', 'empresa', 'dt_criado', 'dt_modificado']
    search_fields = ['user']
    list_filter = ['empresa']
