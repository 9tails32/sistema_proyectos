from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    """
    Funcion de login de usuario. Recibe los datos de usuario en el request y redirecciona la pagina,
    pasando el estado final del login, luego de la autenticacion, dentro del context, al template.
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
            else:
                state = "La cuenta no esta activa. Contacte con el administrador."
        else:
            state = "Su nombre de usuario o password es incorrecto/a."

    return render(request,'login.html',{'state':state, 'username': username})

def logout_user(request):
    logout(request)
    return redirect("/")
