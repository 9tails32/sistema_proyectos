from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Proyecto
from django.utils import timezone
from .forms import *
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django import forms
# Create your views here.


@login_required(None, 'login', '/login/')
@permission_required('proyecto.view_proyecto', raise_exception=True)
def list_proyecto(request):
    """
        Vista que permite displayar un listado de los proyectos existentes.
        """

    queryset = Proyecto.objects.filter(activo=True)
    return render(request, 'proyecto_list.html', {'proyecto_list': queryset})

@login_required(None, 'login', '/login/')
def detail_proyecto(request,pk):
    """
        Vista que permite displayar los detalles de un proyecto seleccionado.
    """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename', flat=True)
    permisos2 = []
    for i in proyecto.equipos.filter(usuarios=request.user.id).distinct():
        permisos2.extend(i.permisos.all())

    if not 'view_proyecto' in permisos and not request.user.is_superuser and not request.user==proyecto.lider_proyecto:
        return HttpResponseRedirect('/proyecto/')

    return render(request, 'proyecto_detail.html', {'object': proyecto,'permisos':permisos,'permisos2':permisos2})

@login_required(None, 'login', '/login/')
@permission_required('proyecto.add_proyecto', raise_exception=True)
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
            p = Proyecto(nombre=cd['nombre'],
                         fecha_inicio=cd['fecha_inicio'], fecha_fin=cd['fecha_fin'],
                         lider_proyecto=cd['lider_proyecto'], cliente=cd['cliente'],
                         descripcion=cd['descripcion'], estado=cd['estado'], observaciones=cd['observaciones'])
            p.save()
            return HttpResponseRedirect('/proyecto/' + str(p.id))
        else:
            return render(request, 'proyecto_create.html', {'form': form})

    else:
        form = ProyectoForm
        return render(request,'proyecto_create.html', {'form': form})

@login_required(None, 'login', '/login/')
@permission_required('proyecto.can_cambiar_estado', raise_exception=True)
def cambiar_estado (request, pk):
    """
        Funcion para actualizar el estado del proyecto utilizando el form CambiarEstadoForm.
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
        form = CambioEstadoForm(request.POST)
        print form
        if form.is_valid():

            cd=form.cleaned_data
            proyecto.estado= cd['estado']
            proyecto.save()
            return HttpResponseRedirect('/proyecto/'+str(proyecto.id))
    else:
        form = CambioEstadoForm(initial={'nombre':proyecto.nombre,
                             'fecha_fin':proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                             'lider_proyecto':proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                             'descripcion': proyecto.descripcion, 'estado': proyecto.estado,
                             'observaciones':proyecto.observaciones})
    return render(request, 'proyecto_create.html', {'form': form,'proyecto':proyecto})


@login_required(None, 'login', '/login/')
@permission_required('proyecto.change_proyecto', raise_exception=True)
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
            return HttpResponseRedirect('/proyecto/'+str(proyecto.id))
    else:
        proyecto = Proyecto.objects.get(pk = pk)
        form = ProyectoForm(initial={'nombre':proyecto.nombre,
                             'fecha_fin':proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                             'lider_proyecto':proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                             'descripcion': proyecto.descripcion, 'estado': proyecto.estado,
                             'observaciones':proyecto.observaciones})
        return render(request, 'proyecto_create.html', {'form': form,'proyecto':proyecto})

@login_required(None, 'login', '/login/')
@permission_required('proyecto.delete_proyecto', raise_exception=True)
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