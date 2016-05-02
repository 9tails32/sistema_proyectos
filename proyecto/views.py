from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Proyecto
from django.utils import timezone
from .forms import ProyectoForm
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django import forms
# Create your views here.

class ListProyecto (ListView):
    """
    Vista generica de django que permite displayar un listado de los proyectos existentes.
    """
    model = Proyecto
    queryset = Proyecto.objects.filter(activo=True)
    template_name = 'proyecto_list.html'

class DetailProyecto(DetailView):
    """
    Vista generica de django que permite displayar los detalles de un proyecto seleccionado.
    """
    model = Proyecto
    template_name = 'proyecto_detail.html'

def create_proyecto (request):
    """
    Funcion para crear proyecto utilizando el form ProyectoForm.
    Recibe en el request el form completado, o displaya uno vacio en caso de que no se llame a
    post. Controla la validez del form antes de guardarlo como un proyecto nuevo en la base de datos.
    Parametros: Recibe el request.
    Retorna:
    -El render del template proyecto_create.html en caso de form vacio o invalido.
    -Redireccion a lista de proyectos si el form es valido

    """
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
    """
        Funcion para actualizar proyecto utilizando el form ProyectoForm.
        Recibe en el request el form completado, o displaya uno con los datos previos del proyecto en
        caso de que no se llame a post. Controla la validez del form antes de guardarlo como un proyecto
         nuevo en la base de datos.
        Parametros: Recibe el request y el pk del proyecto a editar.
        Retorna:
        -El render del template proyecto_create.html en caso de form vacio o invalido.
        -Redireccion a lista de proyectos si el form es valido

    """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            proyecto.nombre= cd['nombre']
            proyecto.fecha_fin= cd['fecha_fin']
            proyecto.fecha_inicio= cd['fecha_inicio']
            proyecto.lider_proyecto=cd['lider_proyecto']
            proyecto.cliente=cd['cliente']
            proyecto.descripcion= cd['descripcion']
            proyecto.estado= cd['estado']
            proyecto.observaciones= cd['observaciones']
            proyecto.save()
            return HttpResponseRedirect('/proyecto/')
    else:
        proyecto = Proyecto.objects.get(pk = pk)
        form = ProyectoForm({'nombre':proyecto.nombre,
                             'fecha_fin':proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                             'lider_proyecto':proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                             'descripcion': proyecto.descripcion, 'estado': proyecto.estado,
                             'observaciones':proyecto.observaciones})
        return render(request, 'proyecto_create.html', {'form': form,'proyecto':proyecto})

def delete_proyecto(request, pk):
    """
    Busca el proyecto con pk igual al que es parametro y cambia su estado activo a False.
    Parametros: recibe el request y el pk del proyecto a eliminar.
    Retorna: Redireccion a lista de proyectos.
    """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    proyecto.activo = False
    proyecto.save()

    return HttpResponseRedirect('/proyecto/')