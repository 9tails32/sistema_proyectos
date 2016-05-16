from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory, BaseFormSet
from US.models import *
from US.forms import *


# Create your views here.
@login_required(None, 'login', '/login/')
@permission_required('US.ver_tipo_US', raise_exception=True)
def detail_tipo_us(request, pk):
    """
        Vista que permite displayar los detalles de un proyecto seleccionado.
    """
    try:
        tipo_us = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/')

    return render(request, 'tipo_us_detail.html', {'object': tipo_us})


@login_required(None, 'login', '/login/')
@permission_required('US.ver_tipo_US', raise_exception=True)
def list_tipo_us(request):
    tipo_us_list = TipoUS.objects.all()
    return render(request, 'tipo_us_list.html', {'tipo_us_list': tipo_us_list})


@login_required(None, 'login', '/login/')
@permission_required('US.crear_tipo_US', raise_exception=True)
def create_tipo(request):
    if request.method == 'POST':
        form = TipoUSForm(request.POST)
        if form.is_valid():
            nombreC = form.cleaned_data['nombre']
            p = TipoUS(nombre=nombreC)
            p.save()

            return HttpResponseRedirect('/us/actividades/' + str(p.id))
    else:
        form = TipoUSForm()

    return render(request, 'tipo_us_create.html', {'form': form}, )


@login_required(None, 'login', '/login/')
@permission_required('US.crear_actividades', raise_exception=True)
def create_actividad(request, pk):
    try:
        tipo = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/create/')

    if request.method == 'POST':
        form = ActividadesForm(request.POST)
        if form.is_valid():
            actividad = Actividades()
            actividad.tipoUS = tipo
            actividad.nombre = form.cleaned_data['nombre']
            actividad.save()

            return HttpResponseRedirect('/us/tipo/' + str(tipo.id))
    else:
        form = ActividadesForm()

    return render(request, 'actividad_create.html', {'form': form})


@login_required(None, 'login', '/login/')
def list_actividades(request, pk):
    try:
        tipo = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/create/')
    actividades_list = Actividades.objects.filter(tipoUS__pk=pk)

    return render(request, 'actividades_list.html', {'actividades_list': actividades_list, 'object': tipo})


@login_required(None, 'login', '/login/')
@permission_required('')
def create_us(request, pk):
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        print 'Error'

    form = USForm(request.POST or None)
    equipos = proyecto.equipos.all()
    usuarios = Usuario.objects.filter(Q(equipos__in=equipos) | Q(lider=proyecto)).distinct()

    form.fields["usuario_asignado"].queryset = usuarios
    if request.method == 'POST':
        if form.is_valid():
            us = US()
            us.proyecto = proyecto
            us.descripcion_corta = form.cleaned_data['descripcion_corta']
            us.descripcion_larga = form.cleaned_data['descripcion_larga']
            us.tiempo_planificado = form.cleaned_data['tiempo_planificado']
            us.valor_negocio = form.cleaned_data['valor_negocio']
            us.urgencia = form.cleaned_data['urgencia']
            us.usuario_asignado = form.cleaned_data['usuario_asignado']
            us.tipoUS = form.cleaned_data['tipoUS']
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))

    return render(request, 'us_create.html', {'form': form}, )


@login_required(None, 'login', '/login/')
@permission_required('tipous.delete_tipous', raise_exception=True)
def delete_actividad(request, pk):
    """
    Busca el proyecto con pk igual al que es parametro y cambia su estado activo a False.
    Parametros: recibe el request y el pk del proyecto a eliminar.
    Retorna: Redireccion a lista de proyectos.
    """
    try:
        actividad = Actividades.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/')
    tipo_us = actividad.tipoUS
    actividad.delete()

    return HttpResponseRedirect('/us/tipo/' + str(tipo_us.id))


@login_required(None, 'login', '/login/')
@permission_required('tipous.delete_tipous', raise_exception=True)
def delete_tipo_us(request, pk):
    """
    Busca el proyecto con pk igual al que es parametro y cambia su estado activo a False.
    Parametros: recibe el request y el pk del proyecto a eliminar.
    Retorna: Redireccion a lista de proyectos.
    """
    try:
        tipo_us = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/')
    if not tipo_us.uss.all():
        tipo_us.delete()

    return HttpResponseRedirect('/us/tipo/')


@login_required(None, 'login', '/login/')
@permission_required('tipous.change_tipous', raise_exception=True)
def update_tipo_us(request, pk):
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
        tipo_us = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/')

    if request.method == 'POST':
        form = TipoUSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            tipo_us.nombre = cd['nombre']
            tipo_us.save()
            return HttpResponseRedirect('/us/tipo/' + str(tipo_us.id))
    else:
        tipo_us = TipoUS.objects.get(pk=pk)
        form = TipoUSForm(initial={'nombre': tipo_us.nombre})

    return render(request, 'tipo_us_create.html', {'form': form, 'tipo_us': tipo_us})


@login_required(None, 'login', '/login/')
def detail_us(request, pk):
    """
        Vista que permite displayar los detalles de un proyecto seleccionado.
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = us.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',
                                                                                           flat=True)

    return render(request, 'us_detail.html', {'object': us, 'permisos': permisos})


@login_required(None, 'login', '/login/')
def delete_us(request, pk):
    """
    Busca el proyecto con pk igual al que es parametro y cambia su estado activo a False.
    Parametros: recibe el request y el pk del proyecto a eliminar.
    Retorna: Redireccion a lista de proyectos.
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')
    proyecto = us.proyecto
    us.delete()

    return HttpResponseRedirect('/proyecto/' + str(proyecto.id))


@login_required(None, 'login', '/login/')
@permission_required('')
def update_us(request, pk):
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    equipos = us.proyecto.equipos.all()
    usuarios = Usuario.objects.filter(Q(equipos__in=equipos) | Q(lider=us.proyecto)).distinct()
    if request.method == 'POST':
        form = USForm(request.POST)
        form.fields["usuario_asignado"].queryset = usuarios
        if form.is_valid():
            us.descripcion_corta = form.cleaned_data['descripcion_corta']
            us.descripcion_larga = form.cleaned_data['descripcion_larga']
            us.tiempo_planificado = form.cleaned_data['tiempo_planificado']
            us.valor_negocio = form.cleaned_data['valor_negocio']
            us.urgencia = form.cleaned_data['urgencia']
            us.usuario_asignado = form.cleaned_data['usuario_asignado']
            us.tipoUS = form.cleaned_data['tipoUS']
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))
    else:
        form = USForm(initial={'descripcion_corta': us.descripcion_corta,
                               'descripcion_larga': us.descripcion_larga,
                               'tiempo_planificado': us.tiempo_planificado,
                               'valor_negocio': us.valor_negocio,
                               'urgencia': us.urgencia,
                               'usuario_asignado': us.usuario_asignado,
                               'tipoUS': us.tipoUS})

    form.fields["usuario_asignado"].queryset = usuarios

    return render(request, 'us_create.html', {'form': form, 'us': us}, )


def cambiar_actividad(request, pk):
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    actividades = us.tipoUS.actividades.all()

    if request.method == 'POST':
        form = CambiarActividadForm(request.POST)
        form.fields['actividad'].queryset = actividades
        if form.is_valid():
            us.actividad = form.cleaned_data['actividad']
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))
    else:
        form = CambiarActividadForm(initial={'actividad': us.actividad})

    form.fields['actividad'].queryset = actividades

    return render(request, 'cambiar_actividad.html', {'form': form, 'us': us})


def cambiar_estado_actividad(request, pk):
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if request.method == 'POST':
        form = CambiarEstadoActividadForm(request.POST)
        if form.is_valid():
            us.estado_actividad = form.cleaned_data['estado_actividad']
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))

    else:
        form = CambiarEstadoActividadForm(initial={'estado_actividad': us.estado_actividad})

    return render(request, 'cambiar_estado_actividad.html', {'form': form, 'us': us})
