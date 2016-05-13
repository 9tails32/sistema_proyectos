from __future__ import unicode_literals

from django.db import models

# Create your models here.
class US(models.Model):
    descripcion_corta = models.TextField(default="")
    descripcion_larga = models.TextField(default="")
    tiempo_planificado = models.IntegerField(default=0)
    valor_negocio = models.IntegerField(default=0) # 0 a 4
    urgencia = models.IntegerField(default=0) # 0 a 4