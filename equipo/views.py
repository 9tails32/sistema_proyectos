from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from proyecto.models import Proyecto
from equipo.models import *
from equipo.forms import *


def enviar_notificacion (email, contenido):
    subject, from_mail, to = 'Sistema de Gestion de Proyectos', 'gmacchi@bellbird.com.py', email
    html_content = '<p>Este mensaje es enviado para notificar sobre lo siguiente:</p><p>'+contenido+'</p>'
    msg = EmailMessage(subject, html_content, from_mail, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


# Create your views here.

@login_required(None, 'login', '/login/')
def create_equipo (request, pk):
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')
    lider = Usuario.objects.get(pk=proyecto.lider_proyecto.pk)
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
            if (lider.noti_creacion_equipos):
                email_noti = lider.email
                enviar_notificacion(email_noti, 'Se ha creado un nuevo equipo y asignado al proyecto "' + proyecto.nombre + '"')
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

