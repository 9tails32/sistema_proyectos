from __future__ import unicode_literals

from django.db import models
from proyecto.models import Proyecto


# Create your models here.
class Sprint(models.Model):
    """
    Clase Sprint que hereda de models.Model
    nombre = Nombre del Sprint.
    duracion = Duracion calculada del Sprint.
    proyecto = Proyecto al que pertenece el Sprint.
    """

    nombre = models.TextField(default='')
    duracion = models.IntegerField(default=0)
    proyecto = models.ForeignKey(Proyecto,null=True,related_name='sprints')

    class Meta:
        permissions = (
            ("ver_sprint", "Puede ver Sprint"),
            ("crear_sprint", "Puede crear un nuevo Sprint"),
        )
    def __unicode__(self):
        return self.nombre
