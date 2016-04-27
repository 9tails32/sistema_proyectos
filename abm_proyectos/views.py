from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proyecto
from django.forms.models import modelform_factory
from django import forms
# Create your views here.

class ListProyecto (ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'


class CreateProyecto (CreateView):
    model = Proyecto
    template_name = 'proyecto_create.html'
    success_url = '/proyecto'
    form_class = modelform_factory(Proyecto, fields = ['nombre', 'fecha_creacion', 'fecha_inicio', 'fecha_fin',
                                                       'lider_proyecto', 'cliente',
                                                        'descripcion', 'estado', 'observaciones'],
                                   widgets={'fecha_inicio': forms.SelectDateWidget(),
                                            'fecha_fin': forms.SelectDateWidget(),
                                            'fecha_creacion': forms.SelectDateWidget()})

class UpdateProyecto (UpdateView):
    model = Proyecto
    template_name = 'proyecto_create.html'
    success_url = '/proyecto'
    form_class = modelform_factory(Proyecto, fields=['nombre', 'fecha_creacion', 'fecha_inicio', 'fecha_fin',
                                                     'lider_proyecto', 'cliente',
                                                     'descripcion', 'estado', 'observaciones'],
                                   widgets={'fecha_inicio': forms.SelectDateWidget(),
                                            'fecha_fin': forms.SelectDateWidget(),
                                            'fecha_creacion': forms.SelectDateWidget()})

