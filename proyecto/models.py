#encoding:utf-8
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.utils import timezone
from django.db import models
from login.models import Usuario
from cliente.models import Cliente

class Proyecto (models.Model):
    """
    Se crea la clase Proyecto, que hereda de Model de django, con los siguientes atributos:
    nombre : El nombre del proyecto.
    fechaCreacion : La fecha en la cual se creo el proyecto.
    fechaInicio : La fecha en la cual se inicia el proyecto.
    fechaFin : La fecha en la cual se termino el proyecto.
    liderProyecto : Usuario lider del proyecto.
    descripcion : breve descripcion del proyecto.
    estado : Estado actual del proyecto, puede ser Pendiente, Anulado, Activo o Finalizado.
    Obvservaciones : Ciertas observaciones del proyecto.
    cliente : Cliente que solicito el proyecto.
    activo : variable que determina un estado de "eliminado" para el Proyecto.


    Metodos:
    hacerLider : Establece un Usuario como lider del proyecto.
    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('ANU', 'Anulado'),
        ('ACT', 'Activo'),
        ('FIN', 'Finalizado'),)
    nombre = models.CharField(max_length=50, null=False)
    fecha_creacion = models.DateField(auto_now=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    lider_proyecto = models.ForeignKey(Usuario, related_name='lider')
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado del proyecto')
    observaciones = models.TextField(max_length=140, null=True, default='No hay observaciones')
    cliente = models.ForeignKey(Cliente, on_delete= models.DO_NOTHING)
    activo = models.BooleanField(default=True)

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
            ("view_proyecto", "Puede ver proyecto"),
            ("change_estado", "Puede cambiar el estado del proyecto"),
            ("view_log", "Puede cambiar el estado del proyecto"),
        )

    def hacerLider (self, lider):
        self.lider_proyecto=lider
        self.save()

    def __unicode__ (self):
        return self.nombre

auditlog.register(Proyecto)