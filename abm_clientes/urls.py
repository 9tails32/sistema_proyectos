from django.conf.urls import url
from .views import ListCliente, CreateCliente, UpdateCliente, DetailCliente

urlpatterns = [
    url(r'^$', ListCliente.as_view()),
    url(r'^create/$',CreateCliente.as_view()),
    url(r'update/(?P<pk>[0-9]+)/$', UpdateCliente.as_view(), name='cliente_update'),
    url(r'^(?P<pk>[0-9]+)/$', DetailCliente.as_view(), name='cliente_detail'),
]