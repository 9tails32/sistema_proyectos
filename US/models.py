from __future__ import unicode_literals

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from proyecto.models import Proyecto
from sprint.models import Sprint
from login.models import Usuario

# Create your models here.


class TipoUS(models.Model):
    """
    Clase TipoUS que hereda de models.Model
    nombre = El nombre del tipo de US
    """
    nombre = models.TextField(default="")

    history = AuditlogHistoryField()
    class Meta:
        permissions = (
            ("ver_tipo_US", "Puede ver tipos de US"),
            ("crear_Tipo_US", "Puede crear Tipos de US"),
        )

    def __unicode__(self):
        return self.nombre



class Actividades(models.Model):
    """
    Clase Actividades que hereda de models.Model
    nombre = Nombre de la actividad
    tipoUS= Tipo dee US al que pertenece la actividad.
    """

    nombre = models.TextField(default="")
    tipoUS = models.ForeignKey(TipoUS, related_name='actividades')
    numero = models.IntegerField(default=0)

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
            ("ver_actividades", "Puede ver actividades"),
            ("crear_actividades", "Puede crear actividades"),
        )

    def __unicode__(self):
        return self.nombre

class US(models.Model):
    """
    Clase US que hereda de models.Model.
    sprint = Sprint al que esta asignado el US.
    proyecto = Proyecto al que pertenece el US.
    descripcion_corta = Descripcion corta del US.
    descripcion_larga = Descripcion larga del US.
    tiempo_planificado = Tiempo aproximado que tomaria terminar el US.
    valor_negocio = Entero que representa el valor del US en el proyecto.
    urgencia = Entero que representa la urgencia para terminar el US.
    tipoUS = Tipo de US del US, define el flujo a utilizar.
    actividad = Actividad actual del US dentro del flujo.
    estado_actividad = Estado de la actividad actual.
    """
    sprint = models.ForeignKey(Sprint, null=True,blank=True, related_name='uss')
    proyecto = models.ForeignKey(Proyecto,null=True,related_name='uss')
    descripcion_corta = models.TextField(default="")
    descripcion_larga = models.TextField(default="")
    tiempo_planificado = models.IntegerField(default=0)
    valor_negocio = models.IntegerField(default=1)  # 0 a 4
    urgencia = models.IntegerField(default=1)  # 0 a 4
    usuario_asignado = models.ForeignKey(Usuario, null=True)

    tipoUS = models.ForeignKey(TipoUS,related_name='uss')

    actividad = models.ForeignKey(Actividades, null=True)
    finalizado = models.BooleanField(default=False)
    options_estado_actividad = (
        ('TOD', 'Todo'),
        ('DOI', 'Doing'),
        ('DON', 'Done')
    )
    estado_actividad = models.CharField(max_length=3, choices=options_estado_actividad, default='TOD')

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
            ("ver_US", "Puede ver US"),
            ("crear_US", "Puede crear US"),
            ("change_actividad","Puede cambiar actividad"),
            ("change_estado_actividad","Puede cambiar el estado de actividad"),

        )

    def __unicode__(self):
        return unicode(self.descripcion_corta)


auditlog.register(TipoUS)
auditlog.register(Actividades)
auditlog.register(US)