from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create/(?P<pk>[0-9]+)/$',create_sprint),
    url(r'^asignar_us/(?P<pk>[0-9]+)/$', asignar_us),
    url(r'^(?P<pk>[0-9]+)/$',detail_sprint,name='sprint_detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$',borrar_sprint,name='borrar_sprint'),
    url(r'^update/(?P<pk>[0-9]+)/$', modificar_sprint, name='modificar_sprint'),

]