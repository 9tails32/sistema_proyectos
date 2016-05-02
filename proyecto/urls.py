from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', ListProyecto.as_view()),
    url(r'^create/$',create_proyecto),
    url(r'update/(?P<pk>[0-9]+)/$', update_proyecto, name='proyecto_update'),
    url(r'delete/(?P<pk>[0-9]+)/$', delete_proyecto, name='proyecto_delete'),
    url(r'^(?P<pk>[0-9]+)/$', DetailProyecto.as_view(), name='proyecto_detail'),

]