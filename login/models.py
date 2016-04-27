from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from abm_clientes.models import Cliente
# Create your models here.

class Usuario (User):
    """
    Se crea la clase Usuario que hereda del modelo User de django, para agregarle mas atributos.
    telefono = Numero de telefono del usuario.
    cedula = numero de cedula del usuario.
    direccion = direccion del usuario.
    """
    cedula = models.PositiveIntegerField(default=0)
    direccion = models.TextField(max_length=50, blank=True, null=False)

    def __unicode__(self):
        return self.username

class Telefono (models.Model):
    numero = models.PositiveIntegerField(default=0)
    cliente = models.ForeignKey(Cliente, null=True)
    usuario = models.ForeignKey(Usuario, null=True)


    def __unicode__(self):
        return self.valor
