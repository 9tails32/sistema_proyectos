import datetime

from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from sprint.models import Sprint
from sprint.forms import *
from proyecto.models import Proyecto
from US.models import US, TipoUS


# Create your views here.
@login_required(None, 'login', '/login/')
@permission_required('sprint.crear_sprint', raise_exception=True)
def create_sprint(request, pk):
    """
        Funcion para crear sprint utilizando el form SprintForm.
        Recibe en el request el form completado o o displaya uno vacio en caso de que no se llame a post,
        y el pk del proyecto al que pertenece el sprint. Controla la validez del form antes de guardarlo
        como un sprint nuevo en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template sprint_create.html en caso de form vacio o invalido.
        -Redireccion a lista de sprint si el form es valido.
        -Error, si no existe el proyecto.

        """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = Sprint()
            sprint.proyecto = proyecto
            sprint.nombre = form.cleaned_data['nombre']
            sprint.fecha_inicio = form.cleaned_data['fecha_inicio']
            sprint.save()
            return HttpResponseRedirect('/proyecto/' + str(proyecto.id))
    else:
        form = SprintForm()

    return render(request, 'sprint_create.html', {'form': form})


@login_required(None, 'login', '/login/')
@permission_required('sprint.ver_sprint', raise_exception=True)
def detail_sprint(request, pk):
    """
        Vista que permite displayar los detalles de un sprint seleccionado.
    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if sprint.duracion > 0:
        sprint.fecha_fin = sprint.fecha_inicio + timedelta(days=sprint.duracion)

    # Aca verificamos si ya inicio el sprint

    if datetime.date.today() <= sprint.fecha_inicio:
        sprint.estado_sprint = 'PEN'
        print 'Proyecto pendiente'
    else:
        print 'Proyecto iniciado'
        sprint.estado_sprint = 'INI'

    # Aca verificamos si ya finalizo
    if sprint.fecha_fin != None:
        if sprint.fecha_fin <= datetime.date.today():
            print 'Proyecto finalizado'
            sprint.estado_sprint = 'FIN'
    sprint.save()

    uss = sprint.uss.all()
    tipos_us = uss.values('tipoUS').distinct()
    tipos = []
    for t in tipos_us:
        tipo_id = t["tipoUS"]
        tipos.append([TipoUS.objects.get(id=tipo_id), uss.filter(tipoUS=tipo_id)])

    return render(request, 'sprint_detail.html', {'sprint': sprint, 'tipos': tipos})


@login_required(None, 'login', '/login/')
@permission_required('proyecto.can_cambiar_estado', raise_exception=True)
def asignar_us(request, pk):
    """
        Funcion para asignar us a un sprint utilizando el form AsignarUSForm.
        Recibe en el request el form completado, o displaya uno con los datos previos del proyecto en
        caso de que no se llame a post. Controla la validez del form antes de asignar el US al Sprint.
        Parametros: Recibe el request y el pk del Sprint a editar.
        Retorna:
        -El render del template asignar_us.html en caso de form vacio o invalido.
        -Redireccion a lista de sprints si el form es valido

    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    uss = US.objects.filter(Q(proyecto=sprint.proyecto, sprint=None) | Q(sprint=sprint))

    if request.method == 'POST':
        form = AsignarUSForm(request.POST)
        form.fields["uss"].queryset = uss
        if form.is_valid():
            sprint.uss = form.cleaned_data['uss']
            acumulador = 0
            for us in sprint.uss.all():
                acumulador += us.tiempo_planificado
            sprint.duracion = acumulador
            sprint.save()

            return HttpResponseRedirect('/sprint/' + str(sprint.id))
    else:
        form = AsignarUSForm(initial={'uss': sprint.uss.all})
        form.fields["uss"].queryset = uss

    return render(request, 'asignar_us.html', {'form': form, 'sprint': sprint})


@login_required(None, 'login', '/login/')
@permission_required('sprint.borrar_sprint', raise_exception=True)
def borrar_sprint(request, pk):
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    sprint.delete()

    return HttpResponseRedirect('/proyecto/')


@login_required(None, 'login', '/login/')
@permission_required('Sprint.change_sprint', raise_exception=True)
def modificar_sprint(request, pk):
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint.nombre = form.cleaned_data['nombre']
            sprint.fecha_inicio = form.cleaned_data['fecha_inicio']
            sprint.save()
            return HttpResponseRedirect('/sprint/' + str(sprint.id))
    else:
        form = SprintForm(initial={'nombre': sprint.nombre,
                                   'fecha_inicio': sprint.fecha_inicio})

        return render(request, 'sprint_create.html', {'form': form, 'sprint': sprint})
