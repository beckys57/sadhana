from django.conf.urls import url
from django.contrib import admin

from . import views

namespace = ''
urlpatterns = [
    url(r'^m/$', views.master_list, name='master_list'),
    url(r'^f/$', views.filtered_list_ajax, name='filter_list'),
    url(r'^l/$', views.make_list_item_ajax, name='make_list_item'),
    #url(r'^p/$', views.create_planting_ajax, name='create_planting'),
    url(r'^ft/$', views.family_tree, name='family_tree'),
    url(r'^r/(?P<person_id>[0-9]+)$', views.define_relationship_ajax, name='define_relationship'),
    url(r'^rtp/(?P<person_id>[0-9]+)$', views.remove_tree_planting_ajax, name='remove_tree_planting'),
    
    url(r'^v/$', views.view_person, name='view_person'),
]
