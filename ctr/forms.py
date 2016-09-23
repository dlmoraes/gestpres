#coding=utf-8
from datetime import datetime
from django import forms
from django.forms.widgets import HiddenInput
from django.forms.models import inlineformset_factory
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from cag.models import Empresa
from cat.models import Pessoa
from .models import *

class TreinamentoForm(forms.ModelForm):

    class Meta:
        model = Treinamento
        fields = ['titulo', 'descricao', 'tipo', 'prazo', 'empresa']

    def __init__(self, *args, **kwargs):
        ocultar = bool(kwargs.pop('ocultar', 'False'))
        empresa = kwargs.pop('empresa', None)
        tipo = kwargs.pop('tipo', 'None')
        super(TreinamentoForm, self).__init__(*args, **kwargs)
        if ocultar:
            if empresa != None:
                self.fields['empresa'].initial = empresa
            self.fields['empresa'].label = ''
            self.fields['empresa'].widget = HiddenInput()
            self.fields['empresa'].widget.attrs = {'readonly': 'false'}
            self.fields['tipo'].initial = tipo
            self.fields['tipo'].label = ''
            self.fields['tipo'].widget = HiddenInput()
            self.fields['tipo'].widget.attrs = {'readonly': 'false'}

class TreinamentoUpdateForm(forms.ModelForm):

    class Meta:
        model = Treinamento
        fields = ['titulo', 'descricao', 'status']

    def __init__(self, *args, **kwargs):
        super(TreinamentoUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['tipo'].initial = tipo
        # self.fields['tipo'].label = ''
        # self.fields['tipo'].widget = HiddenInput()
        # self.fields['status'].disabled = True
        # self.fields['status'].widget.attrs = {'readonly': 'false'}

    def clean(self):

        if 'status' in self.changed_data:
            if self.cleaned_data['status'] == 'CO':
                raise ValidationError({
                    'status': ValidationError(u'Você não tem acesso para alterar o status de treinamento, apenas o sistema ou o administrador.', code='invalid'),
                })
        else:
            if self.cleaned_data['status'] == 'CO':
                raise ValidationError({
                    'status' : ValidationError(u'Não é permitido alterar um treinamento concluído!', code='invalid'),
                })
            elif self.cleaned_data['status'] == 'CA':
                raise ValidationError({
                    'status': ValidationError(u'Não é permitido alterar um treinamento cancelado. Para alterar o status deste treinamento, favor entrar em contato com o administrador do sistema.', code='invalid'),
                })


class MatriculaAvaliacaoForm(forms.ModelForm):

    treinamento = forms.ModelChoiceField(queryset=Treinamento.objects.all(), disabled=True)
    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.all(), disabled=True)

    class Meta:
        model = Matricula
        fields = ['treinamento', 'pessoa']

class MatriculaInicialForm(forms.ModelForm):

    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.filter(pessoa__matricula__isnull=True),
                                    required=True, label='Pessoa')
    class Meta:
        model = Matricula
        fields = ['pessoa']

class MatriculaRotinaForm(forms.ModelForm):

    pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.filter(pessoa__matricula__isnull=False),
                                    required=True, label='Atendente')

    class Meta:
        model = Matricula
        fields = ['pessoa']

class BaseMatriculaFormSet(forms.BaseInlineFormSet):

    def clean(self):

        if any(self.errors):
            return

        pessoas = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                pessoa = form.cleaned_data['pessoa']

                if pessoa in pessoas:
                    duplicates = True
                pessoas.append(pessoa)

                if duplicates:
                    raise forms.ValidationError('Você selecionou a mesma pessoa/atendente, mais de uma vez.')

class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        fields = ['nota', 'prova']

def get_matricula_formset_inicial(form=MatriculaInicialForm, formset=BaseMatriculaFormSet, **kwargs):
    return inlineformset_factory(Treinamento, Matricula, form, formset, extra=1)

def get_matricula_formset_rotina(form=MatriculaRotinaForm, formset=BaseMatriculaFormSet, **kwargs):
    return inlineformset_factory(Treinamento, Matricula, form, formset, extra=1)

def get_avaliacao_formset(form=AvaliacaoForm, formset=forms.BaseInlineFormSet, **kwargs):
    return inlineformset_factory(Matricula, Avaliacao, form, formset, extra=1)