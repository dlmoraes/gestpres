#coding=utf-8

from django import forms
from .models import Perfil

class PerfilModelForm(forms.ModelForm):

    avatar = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = Perfil
        fields = ['user', 'pessoa', 'empresa', 'regional', 'baseregional', 'avatar']
