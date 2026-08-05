# FastAPI Practice Repository

This repository contains a small collection of FastAPI learning projects and practice apps. It is organized as a parent folder with separate mini-projects that demonstrate different concepts such as basic routes, authentication, database integration, API testing, and full-stack web development.

## Projects in this repository

### 1. ToDoApp
Location: [ToDoApp](ToDoApp)

This is the main project in the repository. It is now a full-stack application for managing todos with:

- User registration and login
- JWT-based authentication with cookie-based browser sessions
- Todo CRUD for individual users
- Password and phone number updates
- Admin-only management endpoints
- SQLAlchemy models with PostgreSQL
- Jinja templates and Bootstrap-based frontend pages
- JavaScript-driven client interactions for login, registration, and todo actions

Useful entry points:
- App entry: [ToDoApp/main.py](ToDoApp/main.py)
- Database config: [ToDoApp/database.py](ToDoApp/database.py)
- Browser app: http://127.0.0.1:8000/ after starting the app
- API docs: http://127.0.0.1:8000/docs after starting the app
- Project docs: [ToDoApp/README.md](ToDoApp/README.md)

### 2. practice APIs
Location: [practice APIs](practice%20APIs)

This folder contains smaller practice files used while learning FastAPI basics. These are good references for simple route handling, request models, and quick experiments.

Files include:
- [practice APIs/project_1.py](practice%20APIs/project_1.py)
- [practice APIs/project_2.py](practice%20APIs/project_2.py)

## Quick start from the repository root

### Activate the virtual environment

On Windows PowerShell:

```powershell
.\.fastapi_env\Scripts\Activate.ps1
```

### Run the ToDoApp project

```bash
uvicorn ToDoApp.main:app --reload
```

Then open the app in your browser:

```text
http://127.0.0.1:8000/
```

Or use the API docs:

```text
http://127.0.0.1:8000/docs
```

### Run tests for ToDoApp

```bash
pytest ToDoApp/test -q
```

## Repository structure overview

```text
fastAPI/
├── README.md
├── ToDoApp/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── README.md
│   ├── routers/
│   ├── templates/
│   ├── static/
│   └── test/
└── practice APIs/
    ├── project_1.py
    └── project_2.py
```

## Suggested next steps

- Start with [ToDoApp/README.md](ToDoApp/README.md) for the main application walkthrough
- Explore [practice APIs](practice%20APIs) for beginner-level examples
- Use the Swagger UI to try the API endpoints interactively
