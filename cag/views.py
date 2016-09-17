#coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Empresa, Regional, BaseRegional, TipoAgenciaPex, PontoAtendimento, TipoLink, Agencia

class EmpresaList(LoginRequiredMixin, ListView):

    template_name = 'cag/empresas/empresas.html'
    model = Empresa
    context_object_name = 'empresas'


class RegionalList(LoginRequiredMixin, ListView):

    template_name = 'cag/regionais/regionais.html'
    model = Regional
    context_object_name = 'regionais'

class BaseRegionalList(LoginRequiredMixin, ListView):

    template_name = 'cag/basesregionais/basesregionais.html'
    model = BaseRegional
    context_object_name = 'bases'

class TipoPexList(LoginRequiredMixin, ListView):

    template_name = 'cag/pex/tipos.html'
    model = TipoAgenciaPex
    context_object_name = 'tipos'

class PAList(LoginRequiredMixin, ListView):

    template_name = 'cag/pex/pas.html'
    model = PontoAtendimento
    context_object_name = 'pas'

class DetalheLinkList(LoginRequiredMixin, ListView):

    template_name = 'cag/links/links.html'
    model = TipoLink
    context_object_name = 'links'

class AgenciaList(LoginRequiredMixin, ListView):

    template_name = 'cag/agencias/agencias.html'
    model = Agencia
    context_object_name = 'agencias'

    #def get_queryset(self):
    #    empresa = self.request.user.profile.empresa
    #    return super(AgenciaList, self).get_queryset().filter(empresa=empresa)

class AgenciaDetalhes(LoginRequiredMixin, DetailView):

    template_name = 'cag/agencias/detalhes_agencia.html'
    model = Agencia
    context_object_name = 'agencia'

#    def get_galerias(self):
#        return Galeria.objects.select_related().filter(agencia__pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return super(AgenciaDetalhes, self).get_queryset().prefetch_related('detalhes')

#    def get_context_data(self, **kwargs):
#        context = super(AgenciaDetalhes, self).get_context_data(**kwargs)
#        context['galerias'] = self.get_galerias()
#        return context

empresas = EmpresaList.as_view()
regionais = RegionalList.as_view()
basesregionais = BaseRegionalList.as_view()
tipos = TipoPexList.as_view()
pas = PAList.as_view()
links = DetalheLinkList.as_view()
agencias = AgenciaList.as_view()
agencia_detalhes = AgenciaDetalhes.as_view()