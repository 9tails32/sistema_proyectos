from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login_user(request):
    state = "Please log in below..."
    username = password = ''
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

