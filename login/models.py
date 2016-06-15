from __future__ import unicode_literals

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.auth.models import User, AbstractUser
from django.db import models

from cliente.models import Cliente


# Create your models here.

class Usuario(AbstractUser):
    """
    Se crea la clase Usuario que hereda del modelo User de django, para agregarle mas atributos.
    cedula = numero de cedula del usuario.
    direccion = direccion del usuario.
    """
    cedula = models.PositiveIntegerField(default=0)
    direccion = models.TextField(max_length=50, blank=True, null=False)

    # Configuraciones de usuario
    hora_notificaciones = models.TimeField(null=True, default="00:00:00")
    formato = (
        ('htm', 'HTML'),
        ('txt', 'Texto Plano')
    )
    formato_notificaciones = models.CharField(max_length=3, choices=formato, default='htm', help_text='Formato')
    noti_creacion_proyecto = models.BooleanField(default=False)
    noti_creacion_usuario = models.BooleanField(default=False)
    noti_creacion_equipos = models.BooleanField(default=False)
    noti_cambio_estado_actividades = models.BooleanField(default=False)
    noti_us_asignado = models.BooleanField(default=False)
    noti_cambio_actividades = models.BooleanField(default=False)


    history = AuditlogHistoryField()

    def __unicode__(self):
        return self.username


auditlog.register(Usuario)


class Telefono(models.Model):
    """
    Se crea la clase Telefono que hereda del moodelo Model de django.
    numero : Integer que representa al telefono.
    cliente : CCliente asociado al telefono.
    usuario : Usuario asociado al telefono.

    """
    numero = models.PositiveIntegerField(default=0)
    cliente = models.ForeignKey(Cliente, null=True, related_name="telefonos")
    usuario = models.ForeignKey(Usuario, null=True, related_name="telefonos")

    history = AuditlogHistoryField()

    def __unicode__(self):
        return self.valor


auditlog.register(Telefono)
