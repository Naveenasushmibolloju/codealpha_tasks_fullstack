from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from projects.models import Project
from tasks.models import Task
from .forms import ProjectForm
from notifications.utils import create_notification

# ---------------- DASHBOARD ----------------
def dashboard(request):

    projects = Project.objects.all()

    total_projects = projects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Done').count()
    in_progress_tasks = Task.objects.filter(status='In Progress').count()

    recent_tasks = Task.objects.select_related('project').order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'recent_tasks': recent_tasks,
        'projects': projects,
    })


# ---------------- PROJECT LIST ----------------
def project_list(request):

    projects = Project.objects.all()

    project_data = []

    for project in projects:

        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='Done').count()

        progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        project_data.append({
            'project': project,
            'progress': progress,
            'total_tasks': total_tasks,
        })

    return render(request, 'projects/project_list.html', {
        'project_data': project_data
    })


# ---------------- PROJECT DETAIL ----------------
def project_detail(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    # permission check
    if project.owner != request.user and request.user not in project.members.all():
        return HttpResponseForbidden("Not allowed")

    tasks = project.tasks.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Done").count()
    inprogress_tasks = tasks.filter(status="In Progress").count()
    todo_tasks = tasks.filter(status="Todo").count()

    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render(request, "projects/project_detail.html", {
        "project": project,
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "inprogress_tasks": inprogress_tasks,
        "todo_tasks": todo_tasks,
        "progress": progress,
    })


# ---------------- CREATE PROJECT ----------------
def create_project(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()

            create_notification(
                request.user,
                f"Project '{project.name}' was created successfully."
            )

            return redirect("project_list")

    else:
        form = ProjectForm()

    return render(request, "projects/create_project.html", {"form": form})


# ---------------- EDIT PROJECT ----------------
def edit_project(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            create_notification(
                request.user,
                f"Project '{project.name}' was updated."
            )
            return redirect("project_detail", project_id=project.id)

    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/edit_project.html", {"form": form})


# ---------------- DELETE PROJECT ----------------
def delete_project(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        project_name = project.name
        project.delete()
        create_notification(
            request.user,
            f"Project '{project_name}' was deleted."
        )
        return redirect("project_list")

    return render(request, "projects/delete_project.html", {"project": project})


# ---------------- SEARCH ----------------
def search(request):

    query = request.GET.get('q', '')

    projects = Project.objects.filter(name__icontains=query)
    tasks = Task.objects.filter(title__icontains=query)

    return render(request, "search.html", {
        "projects": projects,
        "tasks": tasks,
        "query": query
    })


# ---------------- ANALYTICS (PLACEHOLDER) ----------------

def analytics(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status="Done").count()

    context = {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
    }

    return render(request, "analytics.html", context)
