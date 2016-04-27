from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Telefono (models.Model):
    valor = models.PositiveIntegerField(default=0)

    def set_valor (v):
        self.valor = v

    def __unicode__(self):
        return self.valor

class Usuario (User):
    """
    Se crea la clase Usuario que hereda del modelo User de django, para agregarle mas atributos.
    telefono = Numero de telefono del usuario.
    cedula = numero de cedula del usuario.
    direccion = direccion del usuario.
    """
    #telefono = models.ForeignKey(Telefono)
    cedula = models.PositiveIntegerField(default=0)
    direccion = models.TextField(max_length=50, blank=True, null=False)

    def __unicode__(self):
        return self.username
