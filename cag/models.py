# coding=utf-8
from django.db import models
from django.urls import reverse_lazy
from core.models import ControleTemporal
from core.lists import SITUACAO_CHOICES
from .lists import UF_CHOICES, CONDICAO_PREDIO_CHOICES

class Empresa(ControleTemporal):
    nome = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='images/empresas', null=True, blank=True)

    class Meta:
        ordering = ['sigla']

    def __str__(self):
        return self.nome

class Regional(ControleTemporal):
    nome = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Regionais'

    def __str__(self):
        return self.nome

    def get_regionais_count(self):
        return self.regionais.count()

class BaseRegional(ControleTemporal):
    nome = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Base Regional'
        verbose_name_plural = 'Bases Regionais'

    def __str__(self):
        return self.nome

    def get_bases_count(self):
        return self.bases.count()

class TipoEstabelecimento(ControleTemporal):
    nome = models.CharField(max_length=35, unique=True)

    class Meta:
        verbose_name = 'Tipo de Estabelecimento'
        verbose_name_plural = 'Tipos de Estabelecimentos'

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(u'Número', max_length=8, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.CharField(u'Município', max_length=100, null=True, blank=True)
    uf = models.CharField('Estado', max_length=2, choices=UF_CHOICES, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

class Contato(models.Model):
    tel_residencial = models.CharField('Telefone residencial', max_length=20, null=True, blank=True)
    tel_celular = models.CharField('Celular', max_length=20, null=True, blank=True)
    email = models.EmailField(u'E-mail', null=True, blank=True)

    class Meta:
        abstract = True

class TipoAgenciaPex(ControleTemporal):
    nome = models.CharField(max_length=25, unique=True)

    class Meta:
        verbose_name = 'Tipo PEX'
        verbose_name_plural = 'Tipos PEX'

    def __str__(self):
        return self.nome

class PontoAtendimento(ControleTemporal):
    tipologia = models.ForeignKey(TipoAgenciaPex, related_name='tipos_pex', null=True, blank=True)
    nome = models.CharField(max_length=10, unique=True)
    qtd = models.PositiveIntegerField('Qtd de pontos')

    class Meta:
        ordering = ['nome']
        verbose_name = u'PA - Ponto de Atendimento'
        verbose_name_plural = u'PAs - Pontos de Atendimentos'

    def __str__(self):
        return self.nome

class TipoLink(ControleTemporal):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Tipo de Link'
        verbose_name_plural = 'Tipos de Link'

    def __str__(self):
        return self.nome

    def get_tiposlinks_count(self):
        return self.links.count()

class HorarioFuncionamento(ControleTemporal):
    entrada1 = models.TimeField('Entrada 1')
    saida1 = models.TimeField(u'Saída 1')
    entrada2 = models.TimeField('Entrada 2', null=True, blank=True)
    saida2 = models.TimeField(u'Saída 2', null=True, blank=True)

    class Meta:
        verbose_name = u'Horário de funcionamento'
        verbose_name_plural = u'Horários de funcionamento'

    def __str__(self):
        retorno = ''
        if not self.entrada2 == None:
            retorno = '{}h às {}h - {}h às {}h'.format(self.entrada1, self.saida1, self.entrada2, self.saida2)
        else:
            retorno = '{}h às {}h'.format(self.entrada1, self.saida1)
        return retorno

class Agencia(ControleTemporal):
    nome = models.CharField(max_length=100, unique=True)
    empresa = models.ForeignKey(Empresa, related_name='emp_ag')
    regional = models.ForeignKey(Regional, related_name='regionais')
    baseregional = models.ForeignKey(BaseRegional, related_name='bases', verbose_name='Base regional')
    situacao = models.CharField(u'Situação', max_length=2, choices=SITUACAO_CHOICES, default='AT')
    is_credenciado = models.BooleanField(u'É credenciado?', default=False)

    class Meta:
        ordering = ['nome']
        verbose_name = u'Agência'
        verbose_name_plural = u'Agências'

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse_lazy('cag:agencia_detalhes', kwargs={'pk': self.pk})

class DetalheAgencia(ControleTemporal, Endereco, Contato):
    agencia = models.OneToOneField(Agencia, related_name='detalhes', primary_key=True)
    uc = models.PositiveIntegerField('Unidade consumidora', null=True, blank=True)
    condicao = models.CharField(u'Condição do prédio', max_length=15, choices=CONDICAO_PREDIO_CHOICES,default='alugado')
    pa = models.ForeignKey(PontoAtendimento, related_name='pas_ag')
    horario = models.ForeignKey(HorarioFuncionamento, related_name='horarios')
    link = models.ForeignKey(TipoLink, related_name='links', null=True, blank=True)

    class Meta:
        verbose_name = u'Detalhe da Agência'
        verbose_name_plural = u'Detalhes das Agências'