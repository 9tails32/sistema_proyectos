from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory, BaseFormSet
from US.models import *
from US.forms import *


# Create your views here.

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

            return HttpResponseRedirect('/us/actividades/' + str(tipo.id))
    else:
        form = ActividadesForm()

    return render(request, 'actividad_create.html', {'form': form})


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
            return HttpResponseRedirect('/us/us' + str(us.id))

    return render(request, 'us_create.html', {'form': form}, )
