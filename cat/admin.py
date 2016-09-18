#coding=utf-8
from django.contrib import admin
from .models import Pessoa, Atendente, Cargo

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dta_nascimento', 'doc_cpf', 'doc_rg']
    search_fields = ['nome', 'doc_cpf', 'doc_rg']
    fieldsets = (
        (None, {
            'fields': ('nome', 'dta_nascimento', 'doc_cpf', 'doc_rg', 'sexo')
        }),
        ('Informações de Localização', {
            'fields': ('logradouro', 'numero', 'bairro', 'municipio', 'uf', 'cep')
        }),
        ('Informações de Contato', {
            'fields': ('tel_residencial', 'tel_celular', 'email')
        }),
    )

@admin.register(Atendente)
class AtendenteAdmin(admin.ModelAdmin):
    pass