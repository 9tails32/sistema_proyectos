#encoding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import models
from proyecto.models import Proyecto
from login.models import Usuario
# Create your models here.


class Equipo(Group):
    """
    Clase Equipo que heredea del modelo Group de django.
    proyecto = proyecto al que pertenece el equipo.
    usuarios = usuarios miembros del equipo.
    """
    proyecto = models.ForeignKey(Proyecto,null=True)
    usuarios = models.ManyToManyField(Usuario)
