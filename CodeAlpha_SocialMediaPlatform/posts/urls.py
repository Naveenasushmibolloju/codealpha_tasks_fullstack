from django.urls import path
from . import views
from .views import delete_post

urlpatterns = [
    path('', views.home),
    path('like/<int:post_id>/', views.like_post),
    path('comment/<int:post_id>/', views.add_comment),
    path(
    'delete-post/<int:post_id>/',
    delete_post,
    name='delete_post'
),
]