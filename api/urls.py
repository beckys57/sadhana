from django.conf.urls import url

from . import views

namespace = 'api'
urlpatterns = [
    url(r'^$', views.planting_data, name='planting_data'),
    url(r'^working$', views.book_list, name='book_list'),
	url(r'^2/$', views.BookList.as_view(), name='book-list'),
]
