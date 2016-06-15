from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import Telefono, Usuario
from proyecto.models import Proyecto
from cliente.forms import TelefonoForm
from login.forms import ConfiguracionForm
from django.db.models import Q


def login_user(request):
    """
    Funcion de login de usuario.

    Variables
    username = Nombre de usuario.
    password = Clave de usuario.
    state = Estado del login, puede ser logueado, esperando datos, o demostrar un error de datos incorrectos.

    La funcion recibe en el request los datos de usuario determina si es correcta y esta activada.
    La funcion retorna por medio del context el estado del login y el username.
    """
    state = ""
    if request.user.is_authenticated():
        state = "Esta logueado como " + str(request.user.username)

    username = password = ""
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Has iniciado sesion correctamente!"
                return redirect('/')
            else:
                state = "La cuenta no esta activa. Contacte con el administrador."
        else:
            state = "Su nombre de usuario o password es incorrecto/a."

    return render(request, 'login.html', {'state': state, 'username': username})


@login_required(None, 'login', '/login/')
def logout_user(request):
    """Funcion que cierra sesion de un usuario y redirecciona a la pantalla de login."""
    logout(request)
    return redirect("/")


@login_required(None, 'login', '/login/')
def dashboard(request):
    """Funcion que muestra el menu principal del sistema"""
    user= request.user
    if user.equipos:
        result = []
        proyectos = Proyecto.objects.filter(Q(activo=True,equipos__in=user.equipos.values('id')) |Q(activo=True,lider_proyecto=user) ).distinct()

        for p in proyectos:
            permisos = []
            equipos = p.equipos.all().values_list('permisos__codename', flat=True)#.filter(usuarios=user.id).distinct().values_list('permisos__codename', flat=True)
            permisos.extend(equipos)
            result.append([p,permisos])

    return render(request, 'dashboard.html', {'proyectos':result})


@login_required(None, 'login', '/login/')
def delete_telefono(request, pk):
    try:
        telefono = Telefono.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/')

    if telefono.cliente:
        aux = telefono.cliente
        telefono.delete()
        return HttpResponseRedirect('/cliente/' + str(aux.id))
    else:
        aux = telefono.usuario
        telefono.delete()
        return HttpResponseRedirect('/usuario/' + str(aux.id))


@login_required(None, 'login', '/login/')
def modificar_telefono(request, pk):
    try:
        t = Telefono.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = TelefonoForm(request.POST)
        if form.is_valid():
            telefono = form.cleaned_data['telefono']
            t.numero = telefono
            t.save()
            if t.cliente:
                return HttpResponseRedirect('/cliente/' + str(t.cliente.id))
            else:
                return HttpResponseRedirect('/usuario/' + str(t.usuario.id))
    else:
        form = TelefonoForm({'telefono': t.numero})

    return render(request, 'edit_telefono.html', {'form': form})

@login_required(None, 'login', '/login/')
def configuracion(request):
    """funcion para la configuracion del sistema"""

    try:
        usuario = Usuario.objects.get(pk=request.user.id)
    except:
        return HttpResponseRedirect('/login/')
    es_lider = False
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data['email_noti']
            usuario.noti_creacion_proyecto = form.cleaned_data['noti_creacion_proyecto']
            usuario.noti_creacion_equipos = form.cleaned_data['noti_creacion_equipo']
            usuario.noti_cambio_estado_actividades = form.cleaned_data['noti_cambio_estado_actividades']
            usuario.noti_cambio_actividades = form.cleaned_data['noti_cambio_actividades']
            usuario.noti_us_asignado = form.cleaned_data['noti_us_asignado']
            usuario.save()
            return HttpResponseRedirect('/')
    else:
        Usuario.objects.get(pk=request.user.id)
        user = request.user

        if user.equipos:

            proyectos = Proyecto.objects.filter(
                Q(activo=True, equipos__in=user.equipos.values('id')) | Q(activo=True, lider_proyecto=user)).distinct()
            if (proyectos.count()>0):
                es_lider=True


        form = ConfiguracionForm(initial={
                                  'email_noti': usuario.email,
                                  'noti_creacion_proyecto': usuario.noti_creacion_proyecto,
                                  'noti_creacion_equipo': usuario.noti_creacion_equipos,
                                  'noti_cambio_actividades': usuario.noti_cambio_actividades,
                                  'noti_cambio_estado_actividades': usuario.noti_cambio_estado_actividades,
                                  'noti_us_asignado':usuario.noti_us_asignado,
                                  })
    return render(request, 'configuracion.html', {'form': form, 'usuario': usuario,'es_lider':es_lider})
