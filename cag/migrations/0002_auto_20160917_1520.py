# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/empresas'),
        ),
    ]
