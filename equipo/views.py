from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from proyecto.models import Proyecto
from equipo.models import *
from equipo.forms import *


# Create your views here.

@login_required(None, 'login', '/login/')
def create_equipo (request, pk):
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = Equipo()
            equipo.proyecto = proyecto
            equipo.nombre = form.cleaned_data['nombre']
            equipo.save()
            equipo.permisos = form.cleaned_data['permisos']
            equipo.usuarios = form.cleaned_data['usuarios']
            equipo.save()
            return  HttpResponseRedirect('/proyecto/'+str(proyecto.id))
    else:
        form = EquipoForm()

    return render(request,'equipo_create.html', {'form': form})

@login_required(None, 'login', '/login/')
def delete_equipo(request, pk):
    try:
        equipo = Equipo.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/')

    proyecto = equipo.proyecto

    equipo.delete()

    return HttpResponseRedirect('/proyecto/'+str(proyecto.id))

