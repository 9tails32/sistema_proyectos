# encoding:utf-8

from __future__ import unicode_literals

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models

from login.models import Usuario
from proyecto.models import Proyecto


# Create your models here.


class Equipo(models.Model):
    """
    Clase Equipo que heredea del modelo Group de django.
    proyecto = proyecto al que pertenece el equipo.
    usuarios = usuarios miembros del equipo.
    """
    nombre = models.CharField(max_length=80)
    permisos = models.ManyToManyField(Permission, blank=True)
    proyecto = models.ForeignKey(Proyecto, null=True, related_name='equipos')
    usuarios = models.ManyToManyField(Usuario, related_name='equipos')

    history = AuditlogHistoryField()

    def __unicode__(self):
        return self.nombre

auditlog.register(Equipo)