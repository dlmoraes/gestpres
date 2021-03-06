# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 00:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cag', '0002_auto_20160917_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('dt_modificado', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('matricula', models.CharField(help_text='A matricula deve ser única.', max_length=15)),
                ('dta_entrevista', models.DateField(blank=True, null=True, verbose_name='Data da entrevista')),
                ('dta_contratacao', models.DateField(blank=True, null=True, verbose_name='Data da contratação')),
                ('dta_desligamento', models.DateField(blank=True, null=True, verbose_name='Data do desligamento')),
                ('situacao', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=2, verbose_name='Situação')),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendentes', to='cag.Agencia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('dt_modificado', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('nome', models.CharField(help_text='O nome do cargo deve ser único', max_length=50, unique=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('dt_modificado', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('logradouro', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.CharField(blank=True, max_length=8, null=True, verbose_name='Número')),
                ('bairro', models.CharField(blank=True, max_length=50, null=True)),
                ('municipio', models.CharField(blank=True, max_length=100, null=True, verbose_name='Município')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AM', 'Amazonas'), ('AP', 'Amapá'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Brasília'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='Estado')),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('tel_residencial', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone residencial')),
                ('tel_celular', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('nome', models.CharField(help_text='Informe o nome completo.', max_length=100)),
                ('dta_nascimento', models.DateField(verbose_name='Data de nascimento')),
                ('doc_cpf', models.CharField(help_text='Informe o CPF', max_length=14, unique=True, verbose_name='CPF')),
                ('doc_rg', models.CharField(help_text='Informe o RG, o registro informado deve ser único', max_length=25, unique=True, verbose_name='RG')),
                ('sexo', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/pessoa/')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.AddField(
            model_name='atendente',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='cat.Cargo'),
        ),
        migrations.AddField(
            model_name='atendente',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pessoa', to='cat.Pessoa'),
        ),
    ]
