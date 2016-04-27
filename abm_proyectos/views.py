from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proyecto
from django.utils import timezone
from .forms import ProyectoForm
from django.http import HttpResponseRedirect
from django.forms.models import modelform_factory
from django import forms
# Create your views here.

class ListProyecto (ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'





def create_proyecto (request):
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


class UpdateProyecto (UpdateView):
    model = Proyecto
    template_name = 'proyecto_create.html'
    success_url = '/proyecto'
    form_class = modelform_factory(Proyecto, fields=['nombre', 'fecha_creacion', 'fecha_inicio', 'fecha_fin',
                                                     'lider_proyecto', 'cliente',
                                                     'descripcion', 'estado', 'observaciones'],
                                   widgets={'fecha_inicio': forms.SelectDateWidget(),
                                            'fecha_fin': forms.SelectDateWidget(),
                                            'fecha_creacion': forms.SelectDateWidget()})

