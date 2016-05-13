# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 15:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipos', to='proyecto.Proyecto'),
        ),
        migrations.AddField(
            model_name='equipo',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
