from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", login_required(views.ProjectListView.as_view()), name="project_list"),
    path("project/create/", login_required(views.ProjectCreateView.as_view()), name="project_create"),
    path("project/<int:pk>/", login_required(views.ProjectDetailView.as_view()), name="project_detail"),
    path("project/<int:pk>/delete/", login_required(views.ProjectDeleteView.as_view()), name="project_delete"),
    path("project/<int:pk>/task/create/", login_required(views.TaskCreateView.as_view()), name="task_create"),
    path("task/<int:pk>/update/", login_required(views.TaskUpdateView.as_view()), name="task_update"),
    path("task/<int:pk>/delete/", login_required(views.TaskDeleteView.as_view()), name="task_delete"),
    path("signup/", views.signup, name="signup"),
]
