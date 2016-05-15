from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create/(?P<pk>[0-9]+)/$',create_sprint),
    url(r'^(?P<pk>[0-9]+)/$',detail_sprint,name='sprint_detail')
]