#coding=utf-8
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Cargo, Pessoa, Atendente

'''class CargoCreate(CreateView):

    template_name = 'cat/cargo/cargo_add.html'
    model = Cargo
    fields = '__all__'
    success_url = reverse_lazy('cat:cargos')
'''
class CargoList(ListView):

    template_name = 'cat/cargos/cargos.html'
    model = Cargo
    paginate_by = 10
    context_object_name = 'cargos'

class PessoaList(ListView):

    template_name = 'cat/pessoas/pessoas.html'
    model = Pessoa
    paginate_by = 10
    context_object_name = 'pessoas'

    def get_queryset(self):
        return super(PessoaList, self).get_queryset().select_related()

class AtendenteList(ListView):

    template_name = 'cat/atendentes/atendentes.html'
    model = Atendente
    paginate_by = 10
    context_object_name = 'atendentes'

    def get_queryset(self):
        return super(AtendenteList, self).get_queryset().select_related('pessoa', 'cargo', 'agencia').all()


# Creates
# add_cargo = CargoCreate.as_view()

# Lists
cargos = CargoList.as_view()
pessoas = PessoaList.as_view()
atendentes = AtendenteList.as_view()