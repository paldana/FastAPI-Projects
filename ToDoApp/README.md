# FastAPI Todo App

This project is a full backend API for managing personal todos with user authentication and role-based access. It supports user registration, login, protected todo CRUD, password updates, phone number updates, and admin-level management of users and todos.

## What the app includes

- User registration and login with JWT-based authentication
- Secure password hashing with `passlib`
- Personal todo CRUD routes that only allow the logged-in user to manage their own items
- Password change and phone number update endpoints
- Admin-only routes for reading and managing all todos and users
- A health check endpoint at `/health`
- SQLAlchemy models backed by PostgreSQL

## Main project files

- `main.py`  
  Creates the FastAPI app, registers all routers, and exposes the health endpoint.

- `database.py`  
  Configures the SQLAlchemy engine and session factory. The app currently uses PostgreSQL.

- `models.py`  
  Defines the `Users` and `Todos` database models.

- `routers/auth.py`  
  Handles user creation, login, JWT token generation, and authentication helpers.

- `routers/todos.py`  
  Provides CRUD endpoints for todos belonging to the current user.

- `routers/users.py`  
  Lets the current user view their profile and change their password or phone number.

- `routers/admin.py`  
  Gives admin users access to manage all todos and users.

- `alembic/`  
  Stores migration configuration and versioned database changes.

- `test/`  
  Contains pytest tests for authentication, admin, todos, and the main app.

## Local development

Run the app from the parent folder of this project, which is the `fastAPI` directory.

### 1. Activate your virtual environment

On Windows PowerShell:

```powershell
.\.fastapi_env\Scripts\Activate.ps1
```

### 2. Make sure PostgreSQL is available

The app expects a PostgreSQL database named `TodoApplicationDatabase` on `localhost`.

If needed, create the database first and adjust the connection string in `ToDoApp/database.py`.

### 3. Start the API

From the parent folder:

```bash
uvicorn ToDoApp.main:app --reload
```

If you prefer to be explicit about the app directory:

```bash
uvicorn ToDoApp.main:app --reload --app-dir .
```

### 4. Open the interactive docs

Once the server is running, open:

```text
http://127.0.0.1:8000/docs
```

You can also use:

```text
http://127.0.0.1:8000/redoc
```

## API flow

1. A client sends a request to the FastAPI app.
2. The request is routed to the correct router.
3. The router uses SQLAlchemy to read or write data.
4. Protected routes validate a JWT bearer token before allowing access.

## Example workflow

- Create a user with `POST /auth/`
- Log in with `POST /auth/token` to obtain a JWT token
- Use the token in the `Authorization` header as `Bearer <token>`
- Create, read, update, or delete todos with the `/todo` endpoints
- Admin users can access `/admin` endpoints to manage all resources

## Testing

Run the test suite from the parent folder:

```bash
pytest ToDoApp/test -q
```

## Notes

- Passwords are hashed before being stored.
- JWT tokens are used to protect private routes.
- Admin access is determined by the `role` field on the user record.
