from django.conf.urls import url

from . import views

namespace = 'api'
urlpatterns = [
    url(r'^2/$', views.book_list, name='master_list'),
	url(r'^$', views.BookList.as_view(), name='book-list'),
]
