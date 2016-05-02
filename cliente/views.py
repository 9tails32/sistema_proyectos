from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import CreateView,ListView,UpdateView, DetailView
from .models import Cliente
from login.models import Telefono
from django.http import HttpResponseRedirect
from .forms import *
# Create your views here.

class ListCliente (ListView):
    model = Cliente
    queryset = Cliente.objects.filter(activo=True)
    template_name = 'cliente_list.html'

class DetailCliente (DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'

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


def create_cliente (request):
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

def update_cliente (request, pk):
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

def delete_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/cliente/')

    cliente.activo = False
    cliente.save()

    return HttpResponseRedirect('/cliente/')
