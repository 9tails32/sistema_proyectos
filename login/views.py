from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

def configuracion(request):
    """Funcion para la configuracion del sistema"""
    return render(request,'configuracion.html',{})