#coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy

from core.models import ControleTemporal

class Perfil(ControleTemporal):
    user = models.OneToOneField(User, related_name='profile')
    pessoa = models.ForeignKey('cat.Pessoa', related_name='pes_user', null=True, blank=True)
    empresa = models.ForeignKey('cag.Empresa', related_name='emp_user', null=True, blank=True)
    regional = models.ForeignKey('cag.Regional', related_name='reg_user', null=True, blank=True)
    baseregional = models.ForeignKey('cag.BaseRegional', related_name='basereg_user', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/usuario/perfil', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse_lazy('accounts:alterar_avatar', kwargs={'pk': self.pk})