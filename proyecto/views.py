from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proyecto
from django.utils import timezone
from .forms import ProyectoForm
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django import forms
# Create your views here.

class ListProyecto (ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'




def create_proyecto (request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            p = Proyecto(nombre=cd['nombre'], fecha_creacion=timezone.now(),
                         fecha_inicio=cd['fecha_inicio'], fecha_fin=cd['fecha_fin'],
                         lider_proyecto=cd['lider_proyecto'], cliente=cd['cliente'],
                         descripcion=cd['descripcion'], estado=cd['estado'], observaciones=cd['observaciones'])
            p.save()
            return HttpResponseRedirect('/proyecto/')
        else:
            return render(request, 'proyecto_create.html', {'form': form})

    else:
        form = ProyectoForm
        return render(request,'proyecto_create.html', {'form': form})

def update_proyecto (request, pk):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            proyecto = Proyecto.objects.get(pk=pk)
            proyecto.nombre= cd['nombre']
            proyecto.fecha_creacion= cd['fecha_creacion']
            proyecto.fecha_fin= cd['fecha_fin']
            proyecto.fecha_inicio= cd['fecha_inicio']
            proyecto.lider_proyecto=cd['lider_proyecto']
            proyecto.cliente=cd['cliente']
            proyecto.descripcion= cd['descripcion']
            proyecto.estado= cd['estado']
            proyecto.observaciones= cd['observaciones']

            return HttpResponseRedirect('/cliente/')
    else:
        proyecto = Proyecto.objects.get(pk = pk)
        form = ProyectoForm({'nombre':proyecto.nombre, 'fecha_creacion':proyecto.fecha_creacion,
                             'fecha_fin':proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                             'lider_proyecto':proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                             'descripcion': proyecto.descripcion, 'estado': proyecto.estado,
                             'observaciones':proyecto.observaciones})
        return render(request, 'cliente_create.html', {'form': form})

