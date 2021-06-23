from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.success),
    path('books/<int:id_book>', views.edit),
    path('delete/<int:id_book>', views.delete),
    path('like/<int:id_book>', views.favorite),
    path('unlike/<int:id_book>', views.unfavorite),

]