from django.conf.urls import url, include
from .views import ListProyecto,create_proyecto, update_proyecto

urlpatterns = [
    url(r'^$', ListProyecto.as_view()),
    url(r'^create/$',create_proyecto),
    url(r'update/(?P<pk>[0-9]+)/$', update_proyecto, name='proyecto_update'),

]