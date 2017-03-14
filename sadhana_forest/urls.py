"""sadhana_forest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from people import urls as people_urls
from people import views as people_views
import trees
from trees import urls as trees_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^people/', include(people_urls, namespace='people')),
    url(r'^trees/', include(trees.urls, namespace='trees')),
    url(r'^people/$', people_views.master_list, name='master_list'),
    
    url(r'^reports/$', people_views.reports, name='reports'),
    
    
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include('api.urls')),
]