from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$', dashboard),
    url(r'^login/', login_user),
    url(r'^logout/', logout_user),
    url(r'configuracion/', configuracion, name='configuracion'),
]