"""
Unit tests for the Task Manager application.
"""
import pytest
from django.contrib.auth.models import User
from tasks.models import Project, Task


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def another_user(db):
    """Create another test user."""
    return User.objects.create_user(username='anotheruser', password='testpass123')


@pytest.fixture
def project(user):
    """Create a test project."""
    return Project.objects.create(
        name='Test Project',
        description='A test project description',
        owner=user
    )


@pytest.fixture
def task(project, user):
    """Create a test task."""
    return Task.objects.create(
        title='Test Task',
        description='A test task description',
        project=project,
        assignee=user,
        status='TODO',
        priority='MEDIUM'
    )


class TestProjectModel:
    """Tests for the Project model."""

    def test_project_creation(self, project):
        """Test that a project is created correctly."""
        assert project.name == 'Test Project'
        assert project.description == 'A test project description'
        assert project.owner is not None

    def test_project_str(self, project):
        """Test the string representation of a project."""
        assert str(project) == 'Test Project'

    def test_project_ordering(self, user):
        """Test that projects are ordered by creation date (newest first)."""
        project1 = Project.objects.create(name='Project 1', owner=user)
        project2 = Project.objects.create(name='Project 2', owner=user)
        projects = Project.objects.filter(owner=user)
        assert projects[0] == project2
        assert projects[1] == project1

    def test_project_completion_percentage_no_tasks(self, project):
        """Test completion percentage with no tasks."""
        assert project.get_completion_percentage() == 0

    def test_project_completion_percentage_with_tasks(self, project, user):
        """Test completion percentage with mixed task statuses."""
        Task.objects.create(title='Task 1', project=project, status='DONE')
        Task.objects.create(title='Task 2', project=project, status='DONE')
        Task.objects.create(title='Task 3', project=project, status='TODO')
        Task.objects.create(title='Task 4', project=project, status='IN_PROGRESS')
        assert project.get_completion_percentage() == 50


class TestTaskModel:
    """Tests for the Task model."""

    def test_task_creation(self, task):
        """Test that a task is created correctly."""
        assert task.title == 'Test Task'
        assert task.description == 'A test task description'
        assert task.status == 'TODO'
        assert task.priority == 'MEDIUM'
        assert task.assignee is not None

    def test_task_str(self, task):
        """Test the string representation of a task."""
        assert str(task) == 'Test Task'

    def test_task_status_choices(self, project):
        """Test that all status choices are valid."""
        for status_code, _ in Task.STATUS_CHOICES:
            task = Task.objects.create(title=f'Task {status_code}', project=project, status=status_code)
            assert task.status == status_code

    def test_task_priority_choices(self, project):
        """Test that all priority choices are valid."""
        for priority_code, _ in Task.PRIORITY_CHOICES:
            task = Task.objects.create(title=f'Task {priority_code}', project=project, priority=priority_code)
            assert task.priority == priority_code

    def test_task_ordering(self, project):
        """Test that tasks are ordered by creation date (newest first)."""
        task1 = Task.objects.create(title='Task 1', project=project)
        task2 = Task.objects.create(title='Task 2', project=project)
        tasks = Task.objects.filter(project=project)
        assert tasks[0] == task2
        assert tasks[1] == task1


class TestProjectTaskRelationship:
    """Tests for the relationship between Projects and Tasks."""

    def test_project_tasks_relationship(self, project, user):
        """Test that tasks belong to a project."""
        Task.objects.create(title='Task 1', project=project, assignee=user)
        Task.objects.create(title='Task 2', project=project, assignee=user)
        Task.objects.create(title='Task 3', project=project, assignee=user)
        assert project.tasks.count() == 3

    def test_cascade_delete_tasks(self, project, user):
        """Test that deleting a project also deletes its tasks."""
        Task.objects.create(title='Task 1', project=project, assignee=user)
        Task.objects.create(title='Task 2', project=project, assignee=user)
        project_id = project.id
        project.delete()
        assert Task.objects.filter(project_id=project_id).count() == 0

    def test_owner_can_have_multiple_projects(self, user):
        """Test that a user can own multiple projects."""
        project1 = Project.objects.create(name='Project 1', owner=user)
        project2 = Project.objects.create(name='Project 2', owner=user)
        assert user.owned_projects.count() == 2


class TestUserTaskAssignment:
    """Tests for task assignment functionality."""

    def test_task_can_be_unassigned(self, project):
        """Test that a task can have no assignee."""
        task = Task.objects.create(title='Unassigned Task', project=project, assignee=None)
        assert task.assignee is None

    def test_task_assignee_relationship(self, project, user, another_user):
        """Test that tasks can be assigned to different users."""
        task1 = Task.objects.create(title='Task 1', project=project, assignee=user)
        task2 = Task.objects.create(title='Task 2', project=project, assignee=another_user)
        assert task1.assignee == user
        assert task2.assignee == another_user

    def test_user_assigned_tasks(self, project, user):
        """Test that we can query tasks assigned to a user."""
        Task.objects.create(title='Task 1', project=project, assignee=user)
        Task.objects.create(title='Task 2', project=project, assignee=user)
        Task.objects.create(title='Task 3', project=project, assignee=None)
        assert user.assigned_tasks.count() == 2
