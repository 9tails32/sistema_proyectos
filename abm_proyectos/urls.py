from django.conf.urls import url, include
from .views import ListProyecto,CreateProyecto, UpdateProyecto

urlpatterns = [
    url(r'^$', ListProyecto.as_view()),
    url(r'^create/$',CreateProyecto.as_view()),
    url(r'update/(?P<pk>[0-9]+)/$', UpdateProyecto.as_view(), name='proyecto_update'),

]