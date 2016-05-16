from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from sprint.models import Sprint
from sprint.forms import *
from proyecto.models import Proyecto


# Create your views here.
@login_required(None, 'login', '/login/')
@permission_required('sprint.crear_sprint', raise_exception=True)
def create_sprint(request, pk):
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
            sprint.save()
            return HttpResponseRedirect('/proyecto/' + str(proyecto.id))
    else:
        form = SprintForm()

    return render(request, 'sprint_create.html', {'form': form})


@login_required(None, 'login', '/login/')
@permission_required('sprint.ver_sprint', raise_exception=True)
def detail_sprint(request,pk):
    """
        Vista que permite displayar los detalles de un proyecto seleccionado.
    """
    try:
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    return render(request, 'sprint_detail.html', {'sprint': sprint})

@login_required(None, 'login', '/login/')
@permission_required('proyecto.can_cambiar_estado', raise_exception=True)
def asignar_us(request, pk):
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
        sprint = Sprint.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    uss = US.objects.filter(Q(proyecto=sprint.proyecto,sprint=None)|Q(sprint=sprint))

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
        form = AsignarUSForm(initial={'uss':sprint.uss.all})
        form.fields["uss"].queryset = uss

    return render(request, 'asignar_us.html', {'form': form, 'sprint': sprint})