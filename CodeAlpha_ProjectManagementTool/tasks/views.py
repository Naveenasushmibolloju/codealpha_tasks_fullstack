from django.shortcuts import render, get_object_or_404
from projects.models import Project
from .models import Task
from django.shortcuts import redirect
from .forms import TaskForm
from .forms import CommentForm
from notifications.utils import create_notification

def kanban_board(request):

    projects = Project.objects.all()

    context = {
    "projects": projects,
    "todo_tasks": Task.objects.filter(status="To Do"),
    "inprogress_tasks": Task.objects.filter(status="In Progress"),
    "review_tasks": Task.objects.filter(status="Review"),
    "done_tasks": Task.objects.filter(status="Done"),
}

    return render(request, "tasks/kanban.html", context)

def task_detail(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    comments = task.comments.all().order_by(
        "-created_at"
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.task = task

            comment.user = request.user

            comment.save()

            message = f"{request.user.username} commented on task '{task.title}'."
            create_notification(request.user, message)

            if task.assigned_to and task.assigned_to != request.user:
                create_notification(task.assigned_to, message)

            return redirect(
                "task_detail",
                task_id=task.id
            )

    else:
        form = CommentForm()

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "comments": comments,
            "form": form,
        }
    )

    
def create_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()

            create_notification(
                request.user,
                f"Task '{task.title}' was created."
            )

            if task.assigned_to and task.assigned_to != request.user:
                create_notification(
                    task.assigned_to,
                    f"You were assigned to task '{task.title}'."
                )

            return redirect('kanban')

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/create_task.html",
        {"form": form}
    )
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            create_notification(
                request.user,
                f"Task '{task.title}' was updated."
            )

            if task.assigned_to and task.assigned_to != request.user:
                create_notification(
                    task.assigned_to,
                    f"Task '{task.title}' assigned to you was updated."
                )

            return redirect('task_detail', task_id=task.id)

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {
            "form": form,
            "task": task
        }
    )
def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task_title = task.title
        assigned_to = task.assigned_to
        task.delete()

        create_notification(
            request.user,
            f"Task '{task_title}' was deleted."
        )

        if assigned_to and assigned_to != request.user:
            create_notification(
                assigned_to,
                f"Task '{task_title}' assigned to you was deleted."
            )

        return redirect("kanban")

    return render(request, "delete_task.html", {
        "task": task
    })
