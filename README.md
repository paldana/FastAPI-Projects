# FastAPI Practice Repository

This repository contains a small collection of FastAPI learning projects and practice apps. It is organized as a parent folder with separate mini-projects that demonstrate different concepts such as basic routes, authentication, database integration, and API testing.

## Projects in this repository

### 1. ToDoApp
Location: [ToDoApp](ToDoApp)

This is the main project in the repository. It is a full FastAPI backend application for managing todos with:

- User registration and login
- JWT-based authentication
- Todo CRUD for individual users
- Password and phone number updates
- Admin-only management endpoints
- SQLAlchemy models with PostgreSQL

Useful entry points:
- App entry: [ToDoApp/main.py](ToDoApp/main.py)
- Database config: [ToDoApp/database.py](ToDoApp/database.py)
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

Then open:

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
│   └── test/
└── practice APIs/
    ├── project_1.py
    └── project_2.py
```

## Suggested next steps

- Start with [ToDoApp/README.md](ToDoApp/README.md) for the main application walkthrough
- Explore [practice APIs](practice%20APIs) for beginner-level examples
- Use the Swagger UI to try the API endpoints interactively
