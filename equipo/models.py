#encoding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import models
from proyecto.models import Proyecto

# Create your models here.


class Equipo(Group):
    proyecto = models.ForeignKey(Proyecto)