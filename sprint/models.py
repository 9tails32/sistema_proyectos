from __future__ import unicode_literals

from django.db import models
from proyecto.models import Proyecto


# Create your models here.
class Sprint(models.Model):
    nombre = models.TextField(default='')
    duracion = models.IntegerField(default=0)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        permissions = (
            ("ver_sprint", "Puede ver Sprint"),
            ("crear_sprint", "Puede crear un nuevo Sprint"),
        )