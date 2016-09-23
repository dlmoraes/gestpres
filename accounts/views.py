#coding=utf-8
import json
import datetime
from django.contrib.admin.models import LogEntry
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from .models import Perfil
from .response import JSONResponse, response_mimetype

class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/perfil.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        perfil = Perfil.objects.select_related('pessoa', 'regional', 'baseregional', 'empresa').prefetch_related('pessoa__pessoa', 'pessoa__pessoa__agencia', 'pessoa__pessoa__cargo').get(user=self.request.user)
        atividades = LogEntry.objects.select_related('content_type').filter(user=self.request.user, action_time__gte=datetime.date.today())
        dados_graf = LogEntry.objects.select_related('user')\
            .filter(user=self.request.user, action_time__year=datetime.date.today().year)\
            .dates('action_time', 'month')\
            .annotate(month=TruncMonth('action_time'))\
            .values('month')\
            .annotate(c=Count('user'))\
            .values('month', 'c').order_by('month')
        context['atividades'] = atividades
        context['dados_graf'] = dados_graf
        context['perfil'] = perfil
        return context

class AlterarAvatar(LoginRequiredMixin, UpdateView):

    template_name = 'accounts/alterar_avatar.html'
    model = Perfil
    fields = ['avatar']

index = IndexView.as_view()
alterar_avatar = AlterarAvatar.as_view()