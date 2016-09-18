# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 02:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cat', '0001_initial'),
        ('cag', '0002_auto_20160917_1520'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('dt_modificado', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/usuario/perfil')),
                ('baseregional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basereg_user', to='cag.BaseRegional')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_user', to='cag.Empresa')),
                ('pessoa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pes_user', to='cat.Pessoa')),
                ('regional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reg_user', to='cag.Regional')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfis',
            },
        ),
    ]
