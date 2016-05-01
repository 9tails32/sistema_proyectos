from __future__ import unicode_literals

from django.db import models
from login.models import Usuario

# Create your models here.


class Configuracion(models.Model):
    usuario = models.ForeignKey(Usuario,related_name="Configuraciones")
    mail = models.EmailField(null=True)
    hora = models.TimeField(null=True)
    formato = (
        ('html','HTML'),
        ('txt','Texto Plano')
    )
    noti_creacion_proyecto = models.BooleanField(name="Notificacion de proyectos creados")
    noti_creacion_usuario = models.BooleanField(name="Notificacion de usuarios creados")
    noti_creacion_equipos = models.BooleanField(name="Notificacion de equipos creados")