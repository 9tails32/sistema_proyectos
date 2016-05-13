from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import CreateView,ListView,UpdateView, DetailView
from cliente.models import Cliente
from login.models import Telefono
from django.http import HttpResponseRedirect
from cliente.forms import *


# Create your views here.
@login_required(None, 'login', '/login/')
@permission_required('cliente.can_view',raise_exception=True)
def list_cliente (request):
    cliente_list = Cliente.objects.filter(activo=True)

    return render(request,'cliente_list.html', {'cliente_list': cliente_list})

@login_required(None, 'login', '/login/')
@permission_required('cliente.can_view',raise_exception=True)
def detail_cliente(request,pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/cliente/')

    return render(request, 'cliente_detail.html', {'object': cliente})


@login_required(None, 'login', '/login/')
@permission_required('login.add_telefono',raise_exception=True)
def create_telefono (request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/cliente/')

    if request.method == 'POST':
        form = TelefonoForm(request.POST)
        if form.is_valid():
            telefono = form.cleaned_data['telefono']
            t = Telefono()
            t.numero = telefono
            t.cliente = cliente
            t.save()
            return HttpResponseRedirect('/cliente/'+str(cliente.id))
    else:
        form = TelefonoForm()

    return render(request,'edit_telefono.html', {'form': form})

@login_required(None, 'login', '/login/')
@permission_required('cliente.add_cliente',raise_exception=True)
def create_cliente (request):
    """
        Funcion para crear cliente utilizando el form ClienteForm.
        Recibe en el request el form completado, o displaya uno vacio en caso de que no se llame a
        post. Controla la validez del form antes de guardarlo como un cliente nuevo en la base de datos.
        Parametros: Recibe el request.
        Retorna:
        -El render del template cliente_create.html en caso de form vacio o invalido.
        -Redireccion a lista de clientes si el form es valido

    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nombreC = form.cleaned_data['nombre']
            direccionC = form.cleaned_data['direccion']
            emailC = form.cleaned_data['email']
            p = Cliente(nombre = nombreC, direccion = direccionC, email= emailC)
            p.save()
            return HttpResponseRedirect('/cliente/'+str(p.id))
    else:
        form = ClienteForm()
    return render(request,'cliente_create.html', {'form': form},context_instance=RequestContext(request))

@login_required(None, 'login', '/login/')
@permission_required('cliente.change_cliente',raise_exception=True)
def update_cliente (request, pk):
    """
        Funcion para actualizar cliente utilizando el form ClienteForm.
        Recibe en el request el form completado, o displaya uno con los datos previos del cliente en
        caso de que no se llame a post. Controla la validez del form antes de guardarlo como un cliente
        nuevo en la base de datos.
        Parametros: Recibe el request y el pk del cliente a editar.
        Retorna:
        -El render del template cliente_create.html en caso de form vacio o invalido.
        -Redireccion a lista de clientes si el form es valido

    """
    try:
        cliente = Cliente.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/cliente/')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente.nombre= form.cleaned_data['nombre']
            cliente.direccion= form.cleaned_data['direccion']
            cliente.email = form.cleaned_data['email']
            cliente.save()
            return HttpResponseRedirect('/cliente/')
    else:
        cliente = Cliente.objects.get(pk = pk)
        form = ClienteForm(initial={'nombre':cliente.nombre, 'direccion':cliente.direccion, 'email':cliente.email})
        return render(request, 'cliente_create.html', {'form': form,'cliente':cliente},context_instance=RequestContext(request))

@login_required(None, 'login', '/login/')
@permission_required('cliente.delete_cliente',raise_exception=True)
def delete_cliente(request, pk):
    """
        Busca el cliente con pk igual al que es parametro y cambia su estado activo a False.
        Parametros: recibe el request y el pk del cliente a eliminar.
        Retorna: Redireccion a lista de clientes.
    """
    try:
        cliente = Cliente.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/cliente/')

    cliente.activo = False
    cliente.save()

    return HttpResponseRedirect('/cliente/')
