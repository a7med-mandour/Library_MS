from django.urls import path
from . import views





urlpatterns= [
    path('', views.index, name= 'index'),
    path('books', views.books, name= 'books'),
    path('delete/<book_name>', views.delete, name= 'delete'),
    path('update/<book_name>', views.update, name= 'update'),

]