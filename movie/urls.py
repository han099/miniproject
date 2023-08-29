from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('movie/info/<int:movie_id>', views.movie_info, name='movie-info'),
    path('movie/input', views.movie_input, name='movie-input'),
    path('', views.movie_list, name='movie-list'),
    path('movie/modify/<int:movie_id>', views.movie_modify, name='movie-modify'),
    path('movie/delete/<int:movie_id>', views.movie_delete, name='movie-delete'),
    path('movie/comment/<int:movie_id>', views.movie_comment, name='movie-comment'),

]
