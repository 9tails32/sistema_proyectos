from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView, DetailView
from .models import Cliente
from django.http import HttpResponseRedirect
from .forms import ClienteForm
# Create your views here.

class ListCliente (ListView):
    model = Cliente
    template_name = 'cliente_list.html'

class DetailCliente (DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'


def create_cliente (request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nombreC = form.cleaned_data['nombre']
            direccionC = form.cleaned_data['direccion']
            emailC = form.cleaned_data['email']
            p = Cliente(nombre = nombreC, direccion = direccionC, email= emailC)
            p.save()
            return HttpResponseRedirect('/cliente/')
    else:
        form = ClienteForm
        return render(request,'cliente_create.html', {'form': form})

def update_cliente (request, pk):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = Cliente.objects.get(pk=pk)
            cliente.nombre= form.cleaned_data['nombre']
            cliente.direccion= form.cleaned_data['direccion']
            cliente.email = form.cleaned_data['email']
            cliente.save()
            return HttpResponseRedirect('/cliente/')
    else:
        cliente = Cliente.objects.get(pk = pk)
        form = ClienteForm({'nombre':cliente.nombre, 'direccion':cliente.direccion, 'email':cliente.email})
        return render(request, 'cliente_create.html', {'form': form})