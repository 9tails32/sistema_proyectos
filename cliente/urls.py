from django.conf.urls import url
from .views import ListCliente, update_cliente, DetailCliente, create_cliente

urlpatterns = [
    url(r'^$', ListCliente.as_view()),
    url(r'^create/$',create_cliente),
    url(r'update/(?P<pk>[0-9]+)/$', update_cliente, name='cliente_update'),
    url(r'^(?P<pk>[0-9]+)/$', DetailCliente.as_view(), name='cliente_detail'),
]