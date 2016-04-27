#encoding:utf-8
from django.utils import timezone
from django.db import models
from login.models import Usuario
from abm_clientes.models import Cliente

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

    Metodos:
    hacerLider : Establece un Usuario como lider del proyecto.
    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('ANU', 'Anulado'),
        ('ACT', 'Activo'),
        ('FIN', 'Finalizado'),)
    nombre = models.CharField(max_length=50, null=False)
    fecha_creacion = models.DateField(default=timezone.now())
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    lider_proyecto = models.ForeignKey(Usuario, related_name='Lider')
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado del proyecto')
    observaciones = models.TextField(max_length=140, null=True, default='No hay observaciones')
    cliente = models.ForeignKey(Cliente, on_delete= models.DO_NOTHING)

    def hacerLider (self, lider):
        self.lider_proyecto=lider
        self.save()

    def __unicode__ (self):
        return self.nombre



