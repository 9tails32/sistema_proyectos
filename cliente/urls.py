from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', list_cliente,name='cliente_list'),
    url(r'^create/$',create_cliente, name='cliente_create'),
    url(r'update/(?P<pk>[0-9]+)/$', update_cliente, name='cliente_update'),
    url(r'add_telefono/(?P<pk>[0-9]+)/$', create_telefono, name='telefono_create'),
    url(r'delete/(?P<pk>[0-9]+)/$', delete_cliente , name='cliente_delete'),
    url(r'^(?P<pk>[0-9]+)/$', detail_cliente, name='cliente_detail'),
]