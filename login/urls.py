from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^login/', views.login_user),
    url(r'^logout/',views.logout_user),
    url(r'^delete_telefono/(?P<pk>[0-9]+)/$', views.delete_telefono, name='delete_telefono'),
    url(r'^modificar_telefono/(?P<pk>[0-9]+)/$', views.modificar_telefono, name='modificar_telefono'),
    url(r'configuracion/',views.configuracion,name='configuracion'),
]