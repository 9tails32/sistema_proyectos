from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from proyecto.models import Proyecto
from equipo.models import *
from equipo.forms import *

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def enviar_notificacion (email, contenido):
    if (validateEmail(email)):
        subject, from_mail, to = 'Sistema de Gestion de Proyectos', 'gmacchi@bellbird.com.py', email
        html_content = '<p>Este mensaje es enviado para notificar sobre lo siguiente:</p><p>'+contenido+'</p>'
        msg = EmailMessage(subject, html_content, from_mail, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

@login_required(None, 'login', '/login/')
def create_equipo (request, pk):
    try:
        proyecto = Proyecto.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',flat=True)
    print request.user.has_perms('equipo.add_equipo')
    print request.user.get_all_permissions()
    if ('update' in permisos or request.user.is_staff or request.user.has_perm('equipo.add_equipo')):
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
    else:
        raise PermissionDenied

@login_required(None, 'login', '/login/')
def delete_equipo(request, pk):
    try:
        equipo = Equipo.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/')

    permisos = equipo.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename', flat=True)
    if ('delete_equipo' in permisos or request.user.is_staff or request.user.has_perm('equipo.delete_equipo')):
        proyecto = equipo.proyecto

        equipo.delete()

        return HttpResponseRedirect('/proyecto/'+str(proyecto.id))
    else:
        raise PermissionDenied

@login_required(None, 'login', '/login/')
def update_equipo(request, pk):
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
        equipo = Equipo.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/proyecto/')

    permisos = equipo.proyecto.equipos.filter(usuarios=request.user.id).distinct().values_list('permisos__codename',flat=True)
    if ('change_equipo' in permisos or request.user.is_staff or request.user.has_perm('equipo.delete_equipo')):
        if request.method == 'POST':
            form = EquipoForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                equipo.nombre = form.cleaned_data['nombre']
                equipo.permisos = form.cleaned_data['permisos']
                equipo.usuarios = form.cleaned_data['usuarios']
                equipo.save()
                return HttpResponseRedirect('/proyecto/' + str(equipo.proyecto.id))
        else:
            form = EquipoForm(initial={'nombre': equipo.nombre,
                                         'permisos': equipo.permisos.all(),
                                         'usuarios': equipo.usuarios.all()})
            return render(request, 'equipo_create.html', {'form': form, 'equipo': equipo})
    else:
        raise PermissionDenied
