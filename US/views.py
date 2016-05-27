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
        Vista que permite displayar los detalles de un US seleccionado.
    """
    try:
        tipo_us = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/')

    return render(request, 'tipo_us_detail.html', {'object': tipo_us})


@login_required(None, 'login', '/login/')
@permission_required('US.ver_tipo_US', raise_exception=True)
def list_tipo_us(request):
    """
        Vista que permite listar los tipos de US.
    """
    tipo_us_list = TipoUS.objects.all()
    return render(request, 'tipo_us_list.html', {'tipo_us_list': tipo_us_list})


@login_required(None, 'login', '/login/')
@permission_required('US.crear_tipo_US', raise_exception=True)
def create_tipo(request):
    """
        Funcion para crear tipo de US utilizando el form TipoUSForm.
        Recibe en el request el form completado, o displaya uno vacio en caso de que no se llame a
        post. Controla la validez del form antes de guardarlo como un tipo nuevo en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template tipo_us_create.html en caso de form vacio o invalido.
        -Redireccion a lista de actividades si el form es valido

        """
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
    """
        Funcion para crear actividad utilizando el form ActividadesForm.
        Recibe en el request el form completado o displaya uno vacio en caso de que no se llame a post,
        y el pk del tipo de us al que pertenecen la actividad. Controla la validez del form antes de
        guardarlo como una actividad nueva en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template actividad_create.html en caso de form vacio o invalido.
        -Redireccion a lista de actividades si el form es valido.
        -Menu de creacion de tipos, si no existe el tipo.

        """
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
            actividad.numero = Actividades.objects.filter(tipoUS__pk=pk).count()+1
            actividad.save()

            return HttpResponseRedirect('/us/tipo/' + str(tipo.id))
    else:
        form = ActividadesForm()

    return render(request, 'actividad_create.html', {'form': form})


@login_required(None, 'login', '/login/')
def list_actividades(request, pk):
    """
        Vista que permite listar las actividades de un tipo de US.
    """
    try:
        tipo = TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/create/')
    actividades_list = Actividades.objects.filter(tipoUS__pk=pk)

    return render(request, 'actividades_list.html', {'actividades_list': actividades_list, 'object': tipo})


@login_required(None, 'login', '/login/')
@permission_required('')
def create_us(request, pk):
    """
        Funcion para crear us utilizando el form USForm.
        Recibe en el request el form completadoo o displaya uno vacio en caso de que no se llame a post,
        y el pk del proyecto al que pertenece el us . Controla la validez del form antes de guardarlo
        como un us nuevo en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template us_create.html en caso de form vacio o invalido.
        -Redireccion a lista de us si el form es valido.
        -Error, si no existe el proyecto.

        """
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
            if (Actividades.objects.filter(tipoUS__pk=us.tipoUS.pk).exists()):
                us.actividad=Actividades.objects.filter(tipoUS__pk=us.tipoUS.pk).get(numero=1)

            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))

    return render(request, 'us_create.html', {'form': form}, )


@login_required(None, 'login', '/login/')
@permission_required('tipous.delete_tipous', raise_exception=True)
def delete_actividad(request, pk):
    """
    Busca la actividad con pk igual al que es parametro y la elimina.
    Parametros: recibe el request y el pk de la actividad a eliminar.
    Retorna: Redireccion a lista de actividades.
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
    Busca el tipo de us con pk igual al que es parametro y elimina si no contiene ningun US.
    Parametros: recibe el request y el pk del tipo a eliminar.
    Retorna: Redireccion a lista de tipos.
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
        Funcion para actualizar tipo de US utilizando el form TipoUSForm.
        Recibe en el request el form completado, o displaya uno con los datos previos del tipo en
        caso de que no se llame a post. Controla la validez del form antes de guardarlo como un tipo
         nuevo en la base de datos.
        Parametros: Recibe el request y el pk del tipo a editar.
        Retorna:
        -El render del template tipo_us_create.html en caso de form vacio o invalido.
        -Redireccion a lista de tipos si el form es valido

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
        Vista que permite displayar los detalles de un us seleccionado.
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = us.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',
                                                                                           flat=True)

    return render(request, 'us_detail.html', {'object': us, 'permisos': permisos})


@login_required(None, 'login', '/login/')
@permission_required('us.delete_us', raise_exception=True)
def delete_us(request, pk):
    """
    Busca el us con pk igual al que es parametro y lo borra.
    Parametros: recibe el request y el pk del us a eliminar.
    Retorna: Redireccion a ldetalle del proyecto.
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')
    proyecto = us.proyecto
    us.delete()

    return HttpResponseRedirect('/proyecto/' + str(proyecto.id))


@login_required(None, 'login', '/login/')
@permission_required('us.crear_us', raise_exception=True)
def update_us(request, pk):
    """
        Funcion para actualizar US utilizando el form USForm.
        Recibe en el request el form completado, o displaya uno con los datos previos del tipo en
        caso de que no se llame a post. Controla la validez del form antes de guardarlo como un US
         nuevo en la base de datos.
        Parametros: Recibe el request y el pk del US a editar.
        Retorna:
        -El render del template us_create.html en caso de form vacio o invalido.
        -Redireccion a lista de IS si el form es valido

    """
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

@login_required(None, 'login', '/login/')
@permission_required('us.change_actividad', raise_exception=True)
def cambiar_actividad(request, pk):
    """
    Funcion que permite al usuario con los permisos adecuados cambiar las actividades y el estado de la actividad de un
    US. Tambien permite finalizar el US.
    :param request:
    :type request:
    :param pk:
    :type pk:
    :return:
    :rtype:
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    actividades = us.tipoUS.actividades.all()

    if request.method == 'POST':
        form = CambiarActividadForm(request.POST)
        form.fields['actividad'].queryset = actividades
        form_estado = CambiarEstadoActividadForm(request.POST)
        finalizado = request.POST.get('finalizado')
        if finalizado == 'Si':
            us.finalizado= True
        else: us.finalizado= False
        if form.is_valid() and form_estado.is_valid():
            us.estado_actividad = form_estado.cleaned_data['estado_actividad']
            us.actividad = form.cleaned_data['actividad']

            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))
    else:
        form = CambiarActividadForm(initial={'actividad': us.actividad})
        form_estado = CambiarEstadoActividadForm(initial={'estado_actividad': us.estado_actividad})
        fin=us.finalizado
    form.fields['actividad'].queryset = actividades

    return render(request, 'cambiar_actividad.html', {'form': form, 'us': us, 'form_estado':form_estado,'fin':fin})

@permission_required('us.change_estado_actividad', raise_exception=True)

def cambiar_estado_actividad(request, pk):
    """
    Funcion que permite cambiar el estado de la actividad actual del US. Permite a usuarios con permisos restringidos
    cambiar el estado de la actividad actual. Sin cambiar de actividad
    :param request:
    :type request:
    :param pk:
    :type pk:
    :return:
    :rtype:
    """
    try:
        us = US.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')
    if  (us.estado_actividad=='TOD'):
        us.estado_actividad='DOI'
        us.save()
        return HttpResponseRedirect('/us/us/' + str(us.id))
    elif (us.estado_actividad=='DOI'):
        us.estado_actividad='DON'
        us.save()
        return HttpResponseRedirect('/us/us/' + str(us.id))
    else:
        """
        actividad_nueva=Actividades.objects.filter(tipoUS__pk=pk).filter(numero__gt=us.actividad.numero).order_by('numero')[0:1]
        if actividad_nueva:
            us.actividad=actividad_nueva[0]
            us.estado_actividad = 'TOD'
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))
        else:"""

        return render(request, 'ultimo_estado.html', {'pk':pk})

    """
    if request.method == 'POST':
        form = CambiarEstadoActividadForm(request.POST)
        if form.is_valid():
            us.estado_actividad = form.cleaned_data['estado_actividad']
            us.save()
            return HttpResponseRedirect('/us/us/' + str(us.id))

    else:
        form = CambiarEstadoActividadForm(initial={'estado_actividad': us.estado_actividad})

    return render(request, 'cambiar_estado_actividad.html', {'form': form, 'us': us})
    """