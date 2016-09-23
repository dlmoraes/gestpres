#coding=utf-8

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.views.generic import TemplateView

from .forms import *
from .models import Treinamento, Matricula

from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views import NamedFormsetsMixin

class AvaliacaoInline(InlineFormSet):
    model = Avaliacao
    fields = ['nota', 'prova']
    extra = 1
    formset_class = get_avaliacao_formset()

    def get_formset(self):
        treinamento = get_object_or_404(Treinamento, pk=self.kwargs.get('treinamento_pk'))
        self.max_num = treinamento.prazo.qtd_prova
        return super(AvaliacaoInline, self).get_formset()

class MatriculaAvaliacao(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    template_name = 'ctr/matriculas/avaliar_matriculado.html'
    model = Matricula
    form_class = MatriculaAvaliacaoForm
    inlines = [AvaliacaoInline]
    inlines_names = ['formset']

    def get_success_url(self):
        return reverse_lazy('ctr:avaliar_treinamento', kwargs=dict(treinamento_pk=self.kwargs.get('treinamento_pk')))


class MatriculaInicialInline(InlineFormSet):
    model = Matricula
    fields = ['pessoa']
    extra = 1
    formset_class = get_matricula_formset_inicial()
    form_class = MatriculaInicialForm

class TreinamentoInicialCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    template_name = 'ctr/matriculas/efetuar_matricula.html'
    model = Treinamento
    form_class = TreinamentoForm
    initial = dict(tipo='inicial')
    inlines = [MatriculaInicialInline]
    inlines_names = ['formset']

    def get_success_url(self):
        return reverse_lazy('ctr:treinamentos')

    def get_context_data(self, **kwargs):
        context = super(TreinamentoInicialCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo treinamento inicial'
        return context

    def get_form_kwargs(self):
        kwargs = super(TreinamentoInicialCreateView, self).get_form_kwargs()
        kwargs['ocultar'] = True
        kwargs['empresa'] = self.request.user.profile.empresa
        return kwargs

class MatriculaRotinaInline(InlineFormSet):
    model = Matricula
    fields = ['pessoa']
    extra = 1
    formset_class = get_matricula_formset_rotina()
    form_class = MatriculaRotinaForm

class TreinamentoRotinaCreateView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    template_name = 'ctr/matriculas/efetuar_matricula.html'
    model = Treinamento
    form_class = TreinamentoForm
    initial = dict(tipo='rotina')
    inlines = [MatriculaRotinaInline]
    inlines_names = ['formset']

    def get_success_url(self):
        return reverse_lazy('ctr:treinamentos')

    def get_context_data(self, **kwargs):
        context = super(TreinamentoRotinaCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Novo treinamento de rotina'
        return context

    def get_form_kwargs(self):
        kwargs = super(TreinamentoRotinaCreateView, self).get_form_kwargs()
        kwargs['ocultar'] = True
        kwargs['empresa'] = self.request.user.profile.empresa
        return kwargs

class TreinamentoInicialUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    template_name = 'ctr/matriculas/update_matricula.html'
    model = Treinamento
    form_class = TreinamentoUpdateForm
    inlines = [MatriculaInicialInline]
    inlines_names = ['formset']

    def get_context_data(self, **kwargs):
        context = super(TreinamentoInicialUpdateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Alterar treinamento inicial'
        return context

    def get_success_url(self):
        return reverse_lazy('ctr:treinamentos')


class TreinamentoRotinaUpdateView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    template_name = 'ctr/matriculas/update_matricula.html'
    model = Treinamento
    form_class = TreinamentoUpdateForm
    inlines = [MatriculaRotinaInline]
    inlines_names = ['formset']

    def get_context_data(self, **kwargs):
        context = super(TreinamentoRotinaUpdateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Alterar treinamento de rotina'
        return context

    def get_success_url(self):
        return reverse_lazy('ctr:treinamentos')

class TreinamentoList(LoginRequiredMixin, ListView):

    template_name = 'ctr/treinamentos/treinamentos.html'
    model = Treinamento
    context_object_name = 'treinamentos'

    def get_queryset(self):
        return super(TreinamentoList, self).get_queryset().prefetch_related('treinamentos').filter(empresa__id=self.request.user.profile.empresa_id)

class MatriculasTreinamentoList(LoginRequiredMixin, ListView):

    template_name = 'ctr/matriculas/matriculas.html'
    model = Matricula
    context_object_name = 'matriculas'

    def get_queryset(self):
        treinamento = get_object_or_404(Treinamento, pk=self.kwargs['treinamento_pk'])
        return super(MatriculasTreinamentoList, self).get_queryset().prefetch_related('matriculas').select_related('treinamento', 'pessoa').filter(treinamento=treinamento)

class MatriculaList(LoginRequiredMixin, ListView):

    template_name = 'ctr/matriculas/pesquisar_matriculas.html'
    model = Matricula
    context_object_name = 'matriculas'

    def get_queryset(self):
        titulo = self.request.GET.get('treinamento', False)
        nome = self.request.GET.get('pessoa', False)
        matricula = self.request.GET.get('matricula', False)

        empresa = self.request.user.profile.empresa_id
        queryset = super(MatriculaList, self).get_queryset().select_related('treinamento', 'pessoa').filter(treinamento__empresa_id=empresa)
        if titulo:
            return queryset.filter(treinamento__titulo__icontains=titulo)
        elif nome:
            return queryset.filter(pessoa__nome__icontains=nome)
        elif matricula:
            return queryset.filter(pessoa__pessoa__matricula__startswith=matricula)
        else:
            return None


treinamentos = TreinamentoList.as_view()
treinamento_inicial_add = TreinamentoInicialCreateView.as_view()
treinamento_inicial_update = TreinamentoInicialUpdateView.as_view()
treinamento_rotina_add = TreinamentoRotinaCreateView.as_view()
treinamento_rotina_update = TreinamentoRotinaUpdateView.as_view()
matriculas_treinamento = MatriculasTreinamentoList.as_view()
avaliar_matriculado = MatriculaAvaliacao.as_view()
pesquisa_matricula = MatriculaList.as_view()