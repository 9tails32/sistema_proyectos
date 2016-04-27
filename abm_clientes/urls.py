from django.conf.urls import url
from .views import ListCliente, CreateCliente, UpdateCliente

urlpatterns = [
    url(r'^$', ListCliente.as_view()),
    url(r'^create/$',CreateCliente.as_view()),
    url(r'update/(?P<pk>[0-9]+)/$', UpdateCliente.as_view(), name='cliente_update'),
]