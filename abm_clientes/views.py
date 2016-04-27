from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView, DetailView
from .models import Cliente
# Create your views here.

class ListCliente (ListView):
    model = Cliente
    template_name = 'cliente_list.html'

class DetailCliente (DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'


class CreateCliente(CreateView):
    model = Cliente
    template_name = 'cliente_create.html'
    success_url = '/cliente'

class UpdateCliente(UpdateView):
    model = Cliente
    fields = ['nombre', 'email', 'direccion']
    template_name = 'cliente_create.html'
    success_url = '/cliente'
