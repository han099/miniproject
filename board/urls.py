from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:post_num>', views.detail_post, name='post-detail'),
    path('detail/<int:post_num>/comment/create', views.create_comment, name='create_comment'),
    # path('board/detail/<int:post_num>/comment/<int:comment_id>/edit', views.edit_comment, name='edit_comment'),
    path('detail/<int:post_num>/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('create', views.create_post, name='post-create'),
    path('board/',views.board,name='board'),
    path('modify/<int:post_num>', views.modify_post, name='post-modify'),
    path('delete/<int:post_num>',views.delete_post,name='post-delete'),

]
