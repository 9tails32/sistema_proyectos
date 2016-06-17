import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from US.models import TipoUS
from login.models import Usuario
from sprint.forms import *
from sprint.models import Sprint


# Create your views here.
@login_required(None, 'login', '/login/')
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

    permisos = proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',flat=True)
    if ('create_sprint' in permisos or request.user.is_staff):
        if request.method == 'POST':
            lider=Usuario.objects.get(pk=proyecto.lider_proyecto.pk)
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
    else:
        raise PermissionDenied




@login_required(None, 'login', '/login/')
def detail_sprint(request, pk):
    """
        Vista que permite displayar los detalles de un sprint seleccionado.

        En esta vista traemos el sprint y verificamos si es que la fecha de inicio ya es igual a la fecha entonces inicia el proyecto
        o lo finaliza respectivamente.

    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = sprint.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename', flat=True)
    if ('create_sprint' in permisos or request.user.is_staff):
        if sprint.duracion > 0:
            sprint.fecha_fin = sprint.fecha_inicio + timedelta(days=sprint.duracion)

        # Aca verificamos si ya inicio el sprint

        if (datetime.date.today() <= sprint.fecha_inicio) and sprint.estado_sprint == 'PEN':
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
    else:
        raise PermissionDenied


@login_required(None, 'login', '/login/')
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

    permisos = sprint.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',
                                                                                               flat=True)
    if ('asignar_us' in permisos or request.user.is_staff):
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
    else:
        raise PermissionDenied


@login_required(None, 'login', '/login/')
def borrar_sprint(request, pk):
    """
    Busca el sprint con pk igual al que es parametro y la elimina.
    Parametros: recibe el request y el pk del sprint a eliminar.
    Retorna: Redireccion a lista de sprints.
    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')
    permisos = sprint.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename', flat=True)
    if ('delete_sprint' in permisos or request.user.is_staff):
        sprint.delete()

        return HttpResponseRedirect('/proyecto/')
    else:
        raise PermissionDenied


@login_required(None, 'login', '/login/')
def modificar_sprint(request, pk):
    """
        Funcion para actualizar sprint utilizando el form SprintForm.
        Recibe en el request el form completado o o displaya uno con los campos anteriores en caso de que
        no se llame a post, y el pk del proyecto al que pertenece el sprint. Controla la validez del form
        antes de guardarlo como un sprint nuevo en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template sprint_create.html en caso de form vacio o invalido.
        -Redireccion a lista de sprint si el form es valido.
        -Error, si no existe el proyecto.

        """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = sprint.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',flat=True)
    if ('delete_sprint' in permisos or request.user.is_staff):
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
    else:
        raise PermissionDenied


@login_required(None, 'login', '/login/')
def iniciar_sprint(request, pk):
    """
    En esta funcion se cambia la fecha de inicio del sprint, la fecha de fin segun la duracion del mismo y se coloca estado iniciado
    :param request:
        Este es el request de la web al view
    :param pk:
        El primary key del sprint actual
    :return:
    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = sprint.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',
                                                                                               flat=True)
    if ('iniciar_sprint' in permisos or request.user.is_staff):
        sprint.fecha_inicio = datetime.date.today()
        sprint.fecha_fin = sprint.fecha_inicio + timedelta(days=sprint.duracion)
        print 'Proyecto iniciado'
        sprint.estado_sprint = 'INI'
        sprint.save()
        return HttpResponseRedirect('/sprint/' + str(sprint.id))
    else:
        raise PermissionDenied


