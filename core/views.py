# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'index.html'

index = IndexView.as_view()