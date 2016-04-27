from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proyecto

# Create your views here.

class ListProyecto (ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'
    def dispatch(self, *args, **kwargs):
        return super(ListProyecto, self).dispatch(*args, **kwargs)

class CreateProyecto (CreateView):
    model = Proyecto
    template_name = 'proyecto_create.html'
    success_url = '/proyecto'
    fields = ['nombre','fechaCreacion','fechaInicio', 'fechaFin','lider_proyecto', 'cliente',
              'descripcion','estado', 'observaciones']

class UpdateProyecto (UpdateView):
    model = Proyecto
    template_name = 'proyecto_create.html'
    success_url = '/proyecto'
    fields = ['nombre', 'fechaCreacion', 'fechaInicio', 'fechaFin', 'lider_proyecto', 'cliente',
              'descripcion', 'estado', 'observaciones']

