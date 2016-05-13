from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Flujo(models.Model):
    nombre=models.TextField(default="")

class Actividad(models.Model):
    nombre=models.TextField(default="")
    estados_actividad= (
        ('TOD','Por hacer'),
        ('DOI','Haciendo'),
        ('DON','Hecho')
    )
    estado=models.CharField(max_length='3',choices=estados_actividad,default='TOD',help_text='Estado de la actividad')