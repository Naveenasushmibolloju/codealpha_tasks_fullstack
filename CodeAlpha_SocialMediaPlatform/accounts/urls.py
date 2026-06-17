from django.urls import path
from .views import register_view, login_view, logout_view, profile_view,follow_unfollow
from .views import edit_profile

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),

    path('profile/<str:username>/', profile_view),
    path('follow/<str:username>/', follow_unfollow),
    path('edit-profile/', edit_profile),
]
