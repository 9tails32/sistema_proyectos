from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', list_proyecto, name='proyecto_list'),
    url(r'^create/$',create_proyecto),
    url(r'update/(?P<pk>[0-9]+)/$', update_proyecto, name='proyecto_update'),
    url(r'cambiar_estado/(?P<pk>[0-9]+)/$', cambiar_estado, name='proyecto_estado'),
    url(r'delete/(?P<pk>[0-9]+)/$', delete_proyecto, name='proyecto_delete'),
    url(r'^(?P<pk>[0-9]+)/$', detail_proyecto, name='proyecto_detail'),

]