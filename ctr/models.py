#coding=utf-8
from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from core.models import ControleTemporal
from core.lists import SITUACAO_CHOICES
from .lists import SITUACAO_AVALIACAO_CHOICES, SITUACAO_TREINAMENTO_CHOICES

class Prazo(ControleTemporal):

    nome = models.CharField(max_length=15, unique=True)
    qtd_dia = models.IntegerField('Quantidade de dias')
    dia_util = models.BooleanField(verbose_name='Dia útil', default=False, help_text='Contabilizar apenas os dias úteis')
    qtd_prova = models.PositiveIntegerField('Quantidade de provas', default=2)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Treinamento(ControleTemporal):

    TIPO_TREINAMENTO = (
        ('inicial', 'Inicial'),
        ('rotina', 'Rotina'),
    )

    titulo = models.CharField('Título', max_length=50, help_text="Deve ter até 50 caracteres.")
    descricao = models.TextField('Descrição', null=True, blank=True)
    tipo = models.CharField(max_length=25, choices=TIPO_TREINAMENTO)
    prazo = models.ForeignKey(Prazo)
    status = models.CharField(max_length=2, choices=SITUACAO_TREINAMENTO_CHOICES, default='EM')
    empresa = models.ForeignKey('cag.Empresa', related_name='emp_tre', null=True, blank=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return '{} [{}]'.format(self.titulo, self.titulo)

    def get_matriculados_count(self):
        return self.treinamentos.count()

    def get_matricular_no_treinamento(self):
        if self.tipo == 'inicial':
            return reverse_lazy('ctr:treinamento_inicial_update', kwargs=dict(pk=self.id))
        else:
            return reverse_lazy('ctr:treinamento_rotina_update', kwargs=dict(pk=self.id))

    def get_ver_matriculados(self):
        return reverse_lazy('ctr:avaliar_treinamento', kwargs=dict(treinamento_pk=self.pk))

class Matricula(ControleTemporal):

    treinamento = models.ForeignKey(Treinamento, related_name='treinamentos')
    pessoa = models.ForeignKey('cat.Pessoa', related_name='pessoas')
    status = models.CharField(max_length=15,
                              choices=SITUACAO_AVALIACAO_CHOICES, default='naoavaliado')

    class Meta:
        ordering = ['treinamento', 'pessoa']
        unique_together = ('treinamento', 'pessoa')

    def __str__(self):
        return '{}'.format(self.pk)

    def get_qtd_provas_lancadas(self):
        return self.matriculas.count()

#    def get_status_matriculado(self):
#        avaliados = self.matriculas.count()
#        if avaliados <= 0:
#            return 'Não avaliado'
#        else:
#            return avaliados

    def get_status(self):
        retorno = None
        if self.status == 'naoavaliado':
            retorno = '<span class="label label-primary label-form">Não avaliado</span>'
        elif self.status == 'aprovado':
            retorno = '<span class="label label-success label-form">Aprovado</span>'
        elif self.status == 'reprovado':
            retorno = '<span class="label label-danger label-form">Reprovado</span>'
        else:
            retorno = '<span class="label label-warning label-form">Recuperação</span>'

    def get_disponibilidade(self):
        lancadas = self.get_qtd_provas_lancadas()
        qtd_prova = self.treinamento.prazo.qtd_prova
        return lancadas >= qtd_prova

    def get_absolute_url(self):
        if self.status != 'aprovado' or self.status != 'reprovado':
            return reverse_lazy('ctr:avaliar_matriculado',
                            kwargs=dict(treinamento_pk=self.treinamento.pk,
                                                                   pk=self.pk
                                        ))

    def save(self, *args, **kwargs):
        super(Matricula, self).save(*args, **kwargs)
        pk_treinamento = self.treinamento_id
        qtd_matriculas_pendentes = Treinamento.objects.filter(pk=pk_treinamento).prefetch_related('treinamentos').filter(treinamentos__status__in=['naoavaliado', 'recuperacao']).count()
        if qtd_matriculas_pendentes == 0:
            treinamento = Treinamento.objects.get(pk=pk_treinamento)
            treinamento.status = 'CO'
            treinamento.save()

class Avaliacao(ControleTemporal):

    matricula = models.ForeignKey(Matricula, related_name='matriculas')
    status = models.CharField(max_length=15,
                              choices=SITUACAO_AVALIACAO_CHOICES, default='naoavaliado')
    nota = models.FloatField('Nota da prova', default=0.00, help_text=u'Informe a nota da prova.')
    prova = models.FileField('Arquivo da prova',
                             upload_to='avaliacoes/provas', help_text=u'Envie a prova.')

    def get_status(self):
        retorno = None
        if self.status == 'naoavaliado':
            retorno = '<span class="label label-primary label-form">Não avaliado</span>'
        elif self.status == 'aprovado':
            retorno = '<span class="label label-success label-form">Aprovado</span>'
        elif self.status == 'reprovado':
            retorno = '<span class="label label-danger label-form">Reprovado</span>'
        else:
            retorno = '<span class="label label-warning label-form">Recuperação</span>'
        return mark_safe(retorno)

    def get_disponibilidade(self):
        lancadas = Avaliacao.objects.filter(matricula=self.matricula).count()
        qtd_prova = self.matricula.treinamento.prazo.qtd_prova
        return lancadas >= qtd_prova

    def get_qtd_provas(self):
        return self.matricula.treinamento.prazo.qtd_prova

    def __str__(self):
        return '{} [{}]'.format(self.matricula, self.status)

    def save(self, *args, **kwargs):
        status = None
        if self.get_disponibilidade():
            raise ValidationError('Não há mais disponibilidade de provas.')
        else:
            # status = None
            pk_matricula = self.matricula_id

            if self.nota >= float(8):
                status = 'aprovado'
            elif self.nota < float(8) and self.matricula.get_qtd_provas_lancadas() == 0:
                status = 'recuperacao'
            else:
                status = 'reprovado'
            self.status = status
        super(Avaliacao, self).save(*args, **kwargs)
        mat = Matricula.objects.get(pk=pk_matricula)
        mat.status = status
        mat.save(force_update=True)



    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'