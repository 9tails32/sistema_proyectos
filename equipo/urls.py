from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'create/(?P<pk>[0-9]+)/$', create_equipo, name='equipo_create'),
    url(r'delete/(?P<pk>[0-9]+)/$', delete_equipo, name='equipo_delete'),
]