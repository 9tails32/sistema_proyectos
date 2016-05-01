#encoding:utf-8
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Cliente (models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField (max_length=100)
    email = models.EmailField()
    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

