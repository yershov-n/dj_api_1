from django.urls import path

from .views import author_create
from .views import author_detail
from .views import author_list
from .views import book_list
from .views import book_create
from .views import book_detail

app_name = 'shelf'


urlpatterns = [
    path('author/', author_list, name='author-list'),
    path('author_add/', author_create, name='author-add'),
    path('author_detail/<int:pk>/', author_detail, name='author-detail'),
    path('book/', book_list, name='book-list'),
    path('book_add/', book_create, name='book-add'),
    path('book_detail/<int:pk>/', book_detail, name='book-detail'),
]
