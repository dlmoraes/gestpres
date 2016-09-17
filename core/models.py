# coding=utf-8
from django.db import models

class ControleTemporal(models.Model):
    dt_criado       = models.DateTimeField('Criado em', auto_now_add=True)
    dt_modificado   = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        abstract = True