# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipo', '0001_initial'),
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='proyecto',

            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.Proyecto'),

        ),
    ]
