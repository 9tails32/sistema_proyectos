from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import Telefono, Usuario
from cliente.forms import TelefonoForm
from login.forms import ConfiguracionForm


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
    return render(request, 'dashboard.html', {})


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
    """funcion paa la configuracion del sistema"""

    try:
        usuario = Usuario.objects.get(pk=request.user.id)
    except:
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':
        form = ConfiguracionForm(request.POST)
        print form.errors
        if form.is_valid():
            print form.cleaned_data['formato_notificaciones']
            usuario.hora_notificaciones = form.cleaned_data['hora_notificaciones']
            usuario.formato_notificaciones = form.cleaned_data['formato_notificaciones']
            usuario.noti_creacion_proyecto = form.cleaned_data['noti_creacion_proyecto']
            usuario.noti_creacion_equipos = form.cleaned_data['noti_creacion_equipo']
            usuario.noti_creacion_usuario = form.cleaned_data['noti_creacion_usuario']
            usuario.save()
            return HttpResponseRedirect('/')
    else:
        usuario = Usuario.objects.get(pk=request.user.id)
        print usuario.formato_notificaciones
        form = ConfiguracionForm(initial={'hora_notificaciones': usuario.hora_notificaciones,
                                  'formato_notificaciones': usuario.formato_notificaciones,
                                  'noti_creacion_proyecto': usuario.noti_creacion_proyecto,
                                  'noti_creacion_usuario': usuario.noti_creacion_usuario,
                                  'noti_creacion_equipo': usuario.noti_creacion_equipos
                                  })
    return render(request, 'configuracion.html', {'form': form, 'usuario': usuario})
