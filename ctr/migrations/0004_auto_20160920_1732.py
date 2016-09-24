# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctr', '0003_treinamento_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='nota',
            field=models.FloatField(default=0.0, help_text='Informe a nota da prova.', verbose_name='Nota da prova'),
        ),
        migrations.AlterField(
            model_name='treinamento',
            name='status',
            field=models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=2),
        ),
    ]