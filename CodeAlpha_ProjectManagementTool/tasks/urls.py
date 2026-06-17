from django.urls import path
from .views import (
    kanban_board,
    task_detail,
    create_task,
    edit_task,
    delete_task
)

urlpatterns = [
    path("kanban/", kanban_board, name="kanban"),
    path("create/", create_task, name="create_task"),
    path("task/<int:task_id>/", task_detail, name="task_detail"),
    path("task/edit/<int:task_id>/", edit_task, name="edit_task"),
    path("task/delete/<int:task_id>/", delete_task, name="delete_task"),
]