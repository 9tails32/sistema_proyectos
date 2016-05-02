from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import Telefono
from cliente.forms import TelefonoForm


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

    return render(request,'login.html',{'state':state, 'username': username})

@login_required(None,'login','/login/')
def logout_user(request):
    """Funcion que cierra sesion de un usuario y redirecciona a la pantalla de login."""
    logout(request)
    return redirect("/")

@login_required(None,'login','/login/')
def dashboard(request):
    """Funcion que muestra el menu principal del sistema"""
    return render(request,'dashboard.html',{})

@login_required(None,'login','/login/')
def delete_telefono(request,pk):
    try:
        telefono = Telefono.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/')

    if telefono.cliente:
        aux = telefono.cliente
        telefono.delete()
        return HttpResponseRedirect('/cliente/'+str(aux.id))
    else:
        aux = telefono.usuario
        telefono.delete()
        return HttpResponseRedirect('/usuario/'+str(aux.id))

@login_required(None,'login','/login/')
def modificar_telefono (request, pk):
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
        form = TelefonoForm({'telefono':t.numero})

    return render(request,'edit_telefono.html', {'form': form})




