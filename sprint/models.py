from __future__ import unicode_literals

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from proyecto.models import Proyecto


# Create your models here.
class Sprint(models.Model):
    """
    Clase Sprint que hereda de models.Model
    nombre = Nombre del Sprint.
    duracion = Duracion calculada del Sprint en dias.
    proyecto = Proyecto al que pertenece el Sprint.
    """

    nombre = models.TextField(default='')
    duracion = models.IntegerField(default=0)
    proyecto = models.ForeignKey(Proyecto, null=True, related_name='sprints')

    options_estado_sprint = (
        ('PEN', 'Pendiente'),
        ('INI', 'Iniciado'),
        ('FIN', 'Finalizado')
    )
    estado_sprint = models.CharField(max_length=3, choices=options_estado_sprint, default='PEN')

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True)

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
            ("view_sprint", "Puede ver Sprint"),
            ("asignar_us", "Puede asignar US al Sprint"),
            ("iniciar_sprint", "Puede iniciar el Sprint"),
        )

    def __unicode__(self):
        return self.nombre


auditlog.register(Sprint)
