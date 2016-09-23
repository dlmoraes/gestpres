#coding=utf-8

from django.contrib import admin
from .models import Prazo, Treinamento, Matricula, Avaliacao

@admin.register(Prazo)
class PrazoAdmin(admin.ModelAdmin):

    list_display = ['nome', 'qtd_dia', 'dia_util', 'dt_criado', 'dt_modificado']
    list_filter = ['dia_util']
    search_fields = ['nome']

class MatriculaInline(admin.StackedInline):
    model = Matricula
    fields = ['pessoa']
    extra = 2

@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    inlines = [MatriculaInline]
    list_display = ['empresa', 'titulo', 'tipo', 'prazo']
    search_fields = ['titulo']
    list_filter = ['empresa', 'tipo', 'prazo']

class AvaliacaoInline(admin.StackedInline):

    model = Avaliacao
    fields = ['nota', 'prova', 'status']
    extra = 1

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):

    inlines = [AvaliacaoInline]
    list_display = ['treinamento', 'pessoa']
