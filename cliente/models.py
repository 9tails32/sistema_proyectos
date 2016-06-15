#encoding:utf-8

from __future__ import unicode_literals

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
# Create your models here.
class Cliente (models.Model):
    """
    Se crea la clase Cliente, que hereda de Model de django, con los siguientes atributos:
    nombre : El nombre del cliente.
    direccion : La direccion el cliente.
    email: Correo electronico del cliente.
    activo: variable que determina un estado de "eliminado" para el Cliente.

    """
    nombre = models.CharField(max_length=100)
    direccion = models.CharField (max_length=100)
    email = models.EmailField()
    activo = models.BooleanField(default=True)

    history = AuditlogHistoryField()

    def __unicode__(self):
        return self.nombre

    class Meta:
        permissions = (
            ("view_cliente", "Puede ver cliente"),
        )

auditlog.register(Cliente)
