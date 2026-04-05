# CI/CD Pipeline for Django - Task Manager

A college project demonstrating a complete CI/CD pipeline for a Python Django web application using GitHub Actions.

## Features

- **User Authentication** - Sign up, login, logout
- **Project Management** - Create, view, and delete projects
- **Task Management** - Create, assign, and track tasks within projects
- **Progress Tracking** - Visual progress bars showing project completion

## CI/CD Pipeline

This project includes a fully automated CI/CD pipeline using GitHub Actions that runs on every push and pull request.

### Pipeline Stages

| Stage | Tool | Description |
|-------|------|-------------|
| Linting | flake8 | Python syntax and style checking |
| Formatting | Black | Code formatting validation |
| Security | Bandit | Security vulnerability scanning |
| Testing | pytest | Unit tests with coverage reporting |
| Dependencies | Safety | Known vulnerability checking |

## Status Badges

![CI Pipeline](https://github.com/SanjayDevarappalli/Updated_CICD/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/SanjayDevarappalli/Updated_CICD/branch/main/graph/badge.svg)](https://codecov.io/gh/SanjayDevarappalli/Updated_CICD)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd CICD_project_django
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://localhost:8000`

## Running Tests Locally

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run linting
flake8 .

# Run code formatting check
black --check .
```

## GitHub Actions

The CI pipeline runs automatically on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

### Viewing CI Results

1. Go to the repository on GitHub
2. Click on the **Actions** tab
3. You'll see the workflow runs with status for each stage

### Updating Status Badges

Replace `YOUR_USERNAME` and `YOUR_REPO` in the badge URLs above with your actual GitHub username and repository name.

## Project Structure

```
CICD_project_django/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── myproject/                # Django project settings
│   ├── settings.py
│   └── urls.py
├── tasks/                    # Main application
│   ├── models.py             # Project, Task models
│   ├── views.py              # CRUD views
│   ├── urls.py               # URL routing
│   └── tests.py              # Unit tests
├── templates/                # HTML templates
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
├── .flake8                   # Flake8 linting config
├── pyproject.toml            # Black & project config
└── manage.py                 # Django management script
```

## Technologies Used

- **Backend**: Django 4.2
- **Testing**: pytest, pytest-django, pytest-cov
- **Linting**: flake8, Black
- **Security**: Bandit, Safety
- **CI/CD**: GitHub Actions

## License

This project is for educational purposes as a college project.
