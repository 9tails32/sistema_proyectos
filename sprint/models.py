from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Sprint(models.Model):
    nombre = models.TextField(default='')
    duracion = models.IntegerField(default=0)