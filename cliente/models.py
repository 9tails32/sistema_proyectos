#encoding:utf-8

from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Cliente (models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField (max_length=100)
    email = models.EmailField()
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


