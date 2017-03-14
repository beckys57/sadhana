from django.conf.urls import url
from django.contrib import admin

from . import views

namespace = 'trees'
urlpatterns = [
    url(r'^d(?P<purpose>[0-9])/$', views.enter_data, name='enter_data')
]
