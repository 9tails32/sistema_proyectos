from django.conf.urls import url, include
from .views import ListProyecto,CreateProyecto

urlpatterns = [
    url(r'^$', ListProyecto.as_view()),
    url(r'^create/$',CreateProyecto.as_view()),
]