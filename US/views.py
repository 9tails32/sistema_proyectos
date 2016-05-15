from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory, BaseFormSet
from US.models import *
from US.forms import *
# Create your views here.

@login_required(None, 'login', '/login/')
@permission_required('US.crear_tipo_US',raise_exception=True)
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

    return render(request, 'tipo_us_create.html', {'form': form},)

@login_required(None, 'login', '/login/')
@permission_required('US.crear_actividades',raise_exception=True)
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

            return HttpResponseRedirect('/us/actividades/'+str(tipo.id))
    else:
        form = ActividadesForm()

    return render(request,'actividad_create.html', {'form': form})

def list_actividades(request, pk):
    try:
        tipo=TipoUS.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/us/tipo/create/')
    actividades_list = Actividades.objects.filter(tipoUS__pk=pk)

    return render(request, 'actividades_list.html', {'actividades_list': actividades_list,'object': tipo})