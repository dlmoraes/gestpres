# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20160923_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(default='images/usuario/no-image.jpg', null=True, upload_to='images/usuario/perfil'),
        ),
    ]