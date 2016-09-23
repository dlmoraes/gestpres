#coding=utf-8
from django.db import models
from django.urls import reverse_lazy
from django.core.validators import RegexValidator

from core.lists import SITUACAO_CHOICES
from core.models import ControleTemporal
from cag.models import Endereco, Contato
from .lists import SEXO_CHOICES

class Cargo(ControleTemporal):
    nome = models.CharField(max_length=50, unique=True, help_text=u'O nome do cargo deve ser único')

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Pessoa(ControleTemporal, Endereco, Contato):
    nome = models.CharField(max_length=100, help_text='Informe o nome completo.')
    dta_nascimento = models.DateField('Data de nascimento')
    doc_cpf = models.CharField('CPF', max_length=14, unique=True, help_text='Informe o CPF', validators=[RegexValidator(regex="[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}")])
    doc_rg = models.CharField('RG', max_length=25, unique=True, help_text=u'Informe o RG, o registro informado deve ser único')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True)
    foto = models.ImageField(upload_to='images/pessoa/', null=True, blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def is_atendente(self):
        return self.pessoa != None


    def get_absolute_url(self):
        pass
        #return reverse_lazy()

class Atendente(ControleTemporal):
    pessoa = models.OneToOneField(Pessoa, related_name='pessoa')
    matricula = models.CharField(max_length=15, help_text=u'A matricula deve ser única.')
    dta_entrevista = models.DateField('Data da entrevista', null=True, blank=True)
    dta_contratacao = models.DateField(u'Data da contratação', null=True, blank=True)
    dta_desligamento = models.DateField('Data do desligamento', null=True, blank=True)
    cargo = models.ForeignKey(Cargo, related_name='cargos')
    situacao = models.CharField(u'Situação', max_length=2, choices=SITUACAO_CHOICES, default='AT')
    agencia = models.ForeignKey('cag.Agencia', related_name='atendentes')

    def __str__(self):
        return self.pessoa.nome

