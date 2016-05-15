from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from sprint.models import Sprint
from sprint.forms import SprintForm
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

