from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Project, Task


class ProjectListView(ListView):
    model = Project
    template_name = "tasks/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tasks/project_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "tasks/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "tasks/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_form.html"
    fields = ["title", "description", "assignee", "status", "priority", "due_date"]

    def get_initial(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"], owner=self.request.user)
        return {"project": project}

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.project.pk})

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["pk"], owner=self.request.user)
        form.instance.project = project
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasks/task_form.html"
    fields = ["title", "description", "assignee", "status", "priority", "due_date"]

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.project.pk})

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.project.pk})

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("project_list")
    else:
        form = UserCreationForm()
    return render(request, "tasks/signup.html", {"form": form})
