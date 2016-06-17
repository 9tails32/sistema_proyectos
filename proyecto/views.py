import datetime
from auditlog.models import LogEntry
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render

from US.models import TipoUS
from proyecto.forms import *
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django import forms
from equipo.views import enviar_notificacion
from proyecto.models import Proyecto


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
def detail_proyecto(request, pk):
    """
        Vista que permite displayar los detalles de un proyecto seleccionado.
    """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    # Aca verificamos si ya inicio el proyecto
    if (proyecto.estado!='ANU' and proyecto.estado!='FIN'):
        if (datetime.date.today() <= proyecto.fecha_inicio):
            if proyecto.estado == 'PEN':
                proyecto.estado = 'PEN'
            else:
                print 'Proyecto iniciado'
                proyecto.estado = 'ACT'

        # Aca verificamos si ya finalizo
        if proyecto.fecha_fin < datetime.date.today():
            print 'Proyecto finalizado'
            proyecto.estado = 'FIN'
    proyecto.save()
    permisos = proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename', flat=True)

    tipoUS = TipoUS.objects.all()

    if not 'view_proyecto' in permisos and not request.user.is_superuser and \
            not request.user == proyecto.lider_proyecto and not request.user.has_perm('proyecto.view_proyecto'):
        raise PermissionDenied
    if proyecto.estado == 'FIN' or proyecto.estado=='ANU' :
        bloqueo='SI'
    else:
        bloqueo='NO'
    print bloqueo
    return render(request, 'proyecto_detail.html', {'object': proyecto, 'permisos': permisos, 'tipoUS': tipoUS,
                                                    'bloqueo':bloqueo})


@login_required(None, 'login', '/login/')
@permission_required('proyecto.add_proyecto', raise_exception=True)
def create_proyecto(request):
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
            cd = form.cleaned_data
            p = Proyecto(nombre=cd['nombre'],
                         fecha_inicio=cd['fecha_inicio'], fecha_fin=cd['fecha_fin'],
                         lider_proyecto=cd['lider_proyecto'], cliente=cd['cliente'],
                         descripcion=cd['descripcion'], observaciones=cd['observaciones'])
            p.save()
            lider=p.lider_proyecto
            if (lider.noti_creacion_proyecto):
                email_noti = lider.email
                enviar_notificacion(email_noti,
                                    'Se te ha asignado como lider del proyecto "' + p.nombre + '"')

            return HttpResponseRedirect('/proyecto/' + str(p.id))
        else:
            return render(request, 'proyecto_create.html', {'form': form})

    else:
        form = ProyectoForm
        return render(request, 'proyecto_create.html', {'form': form})


@login_required(None, 'login', '/login/')
def cambiar_estado(request, pk):
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
            cd = form.cleaned_data
            proyecto.estado = cd['estado']
            proyecto.save()
            return HttpResponseRedirect('/proyecto/' + str(proyecto.id))
    else:
        form = CambioEstadoForm(initial={'nombre': proyecto.nombre,
                                         'fecha_fin': proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                                         'lider_proyecto': proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                                         'descripcion': proyecto.descripcion, 'estado': proyecto.estado,
                                         'observaciones': proyecto.observaciones})
    return render(request, 'proyecto_create.html', {'form': form, 'proyecto': proyecto})


@login_required(None, 'login', '/login/')
def update_proyecto(request, pk):
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
            cd = form.cleaned_data
            proyecto.nombre = cd['nombre']
            proyecto.fecha_fin = cd['fecha_fin']
            proyecto.fecha_inicio = cd['fecha_inicio']
            proyecto.lider_proyecto = cd['lider_proyecto']
            proyecto.cliente = cd['cliente']
            proyecto.descripcion = cd['descripcion']
            proyecto.observaciones = cd['observaciones']
            proyecto.save()
            lider = proyecto.lider_proyecto
            if (lider.noti_creacion_proyecto):
                email_noti = lider.email
                enviar_notificacion(email_noti,
                                    'Se te ha asignado como lider del proyecto "' + proyecto.nombre + '"')
            return HttpResponseRedirect('/proyecto/' + str(proyecto.id))
    else:
        proyecto = Proyecto.objects.get(pk=pk)
        form = ProyectoForm(initial={'nombre': proyecto.nombre,
                                     'fecha_fin': proyecto.fecha_fin, 'fecha_inicio': proyecto.fecha_inicio,
                                     'lider_proyecto': proyecto.lider_proyecto, 'cliente': proyecto.cliente,
                                     'descripcion': proyecto.descripcion,
                                     'observaciones': proyecto.observaciones})
        return render(request, 'proyecto_create.html', {'form': form, 'proyecto': proyecto})


@login_required(None, 'login', '/login/')
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


@login_required(None, 'login', '/login/')
def log_proyecto(request, pk):
    """
    Funcion que displaya el log de las actividades realizadas en el proyecto. Recibe el pk del
    Proyecto sobre el cual se quiere revisar el log.
    :param request:
    :type request:
    :param pk:
    :type pk:
    :return:
    :rtype:
    """
    try:
        proyecto = Proyecto.objects.get(pk=pk)
        log = list(LogEntry.objects.get_for_object(proyecto))

        equipos = proyecto.equipos.all()

        log_equipos = list(LogEntry.objects.get_for_objects(equipos))
        log.extend(log_equipos)

        sprints = proyecto.sprints.all()
        log_sprints = list(LogEntry.objects.get_for_objects(sprints))
        log.extend(log_sprints)

        uss = proyecto.uss.all()
        log_uss = list(LogEntry.objects.get_for_objects(uss))
        log.extend(log_uss)

    except:
        return HttpResponseRedirect('/proyecto/')

    return render(request, 'log_proyecto.html', {'log_proyecto': log})
