from django.urls import path
from .views import dashboard, project_list, search, analytics
from .views import create_project
from .views import project_detail
from .views import edit_project, delete_project
from notifications.views import mark_all_read, notification_list
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('projects/', project_list, name='project_list'),

    path('analytics/', analytics, name='analytics'),
    path('notifications/', notification_list, name='notifications'),
    path('notifications/read/', mark_all_read, name='mark_notifications_read'),

    path('search/', search, name='search'),
    path('projects/create/',create_project,name='create_project'),
    path('projects/<int:project_id>/',project_detail,name='project_detail'),
    path('projects/edit/<int:project_id>/',edit_project,name='edit_project'),
    path('projects/delete/<int:project_id>/',delete_project,name='delete_project'),   
]
