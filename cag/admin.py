#coding=utf-8
from django.contrib import admin
from .models import Empresa, Regional, BaseRegional, TipoEstabelecimento, TipoAgenciaPex, TipoLink, HorarioFuncionamento, Agencia, DetalheAgencia, PontoAtendimento

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):

    list_display = ['nome', 'sigla', 'dt_criado', 'dt_modificado']
    search_fields = ['nome', 'sigla']

@admin.register(Regional)
class RegionalAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

@admin.register(BaseRegional)
class BaseRegionalAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

@admin.register(TipoEstabelecimento)
class TipoEstabelecimentoAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

@admin.register(TipoAgenciaPex)
class TipoAgenciaPexAdmin(admin.ModelAdmin):

    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

'''class DetalheLinkInline(admin.StackedInline):

    model = DetalheLink
    extra = 1
'''
@admin.register(TipoLink)
class TipoLinkAdmin(admin.ModelAdmin):

   # inlines = [DetalheLinkInline]
    list_display = ['nome', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']

@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):

    list_display = ['entrada1', 'saida1', 'entrada2', 'saida2']

@admin.register(PontoAtendimento)
class PontoAtendimentoAdmin(admin.ModelAdmin):

    list_display = ['tipologia', 'nome', 'qtd', 'dt_criado', 'dt_modificado']
    search_fields = ['nome']
    list_filter = ['tipologia']

class DetalheAgenciaInline(admin.StackedInline):

    model = DetalheAgencia
    extra = 1
    max_num = 1
    fieldsets = (
        (None, {
            'fields': ('uc', 'condicao', 'horario', 'link')
        }),
        ('Informações de Localização', {
            'fields': ('logradouro', 'numero', 'bairro', 'municipio', 'uf', 'cep')
        }),
        ('Informações de Contato', {
            'fields': ('tel_residencial', 'tel_celular', 'email')
        }),
        ('PEX', {
            'fields': ('pa',)
        }),
    )

@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):

    inlines = [DetalheAgenciaInline]
    list_display = ['nome', 'regional', 'baseregional', 'empresa', 'situacao']
