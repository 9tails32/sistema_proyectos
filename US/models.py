from __future__ import unicode_literals

from django.db import models
from proyecto.models import Proyecto
from sprint.models import Sprint

# Create your models here.


class TipoUS(models.Model):
    nombre = models.TextField(default="")


class Actividades(models.Model):
    nombre = models.TextField(default="")
    tipoUS = models.ForeignKey(TipoUS)


class US(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    sprint = models.ForeignKey(Sprint, null=True)
    descripcion_corta = models.TextField(default="")
    descripcion_larga = models.TextField(default="")
    tiempo_planificado = models.IntegerField(default=0)
    valor_negocio = models.IntegerField(default=0)  # 0 a 4
    urgencia = models.IntegerField(default=0)  # 0 a 4

    tipoUS = models.ForeignKey(TipoUS)

    actividad = models.ForeignKey(Actividades, limit_choices_to={'tipoUS': tipoUS})

    options_estado_actividad = (
        ('TOD', 'Todo'),
        ('DOI', 'Doing'),
        ('DON', 'Done')
    )
    estado_actividad = models.CharField(max_length=3, choices=options_estado_actividad, default='TOD')
