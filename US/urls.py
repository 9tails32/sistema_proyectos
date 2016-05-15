from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^tipo/create/$',create_tipo),
    url(r'^actividades/create/(?P<pk>[0-9]+)/$', create_actividad, name='actividad_create'),
    url(r'^actividades/(?P<pk>[0-9]+)/$', list_actividades, name='actividad_list'),
    url(r'^us/create/(?P<pk>[0-9]+)/$', create_us, name='us_create'),



]