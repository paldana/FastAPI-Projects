from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.users import bcrypt_context
import pytest

# Create a new SQLite3 in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# Create a new sessionmaker for the testing database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the testing database
Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_current_user dependency to return a test user
def override_get_current_user():
    return {'username': 'test_user', 'id': 1, 'role': 'admin'}


# Create a TestClient for the FastAPI app
client = TestClient(app)

# Create a fixture to set up and tear down test data - runs before and after each test function
@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo", 
        description="This is a test todo", 
        priority=1, 
        complete=False, 
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    # wait for the the test function to run, then continue with the teardown
    yield todo  

    # Clean up the test data after the test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))  # Clean up the test data after the test3
        connection.commit()  # Commit the changes to the database

# Create a fixture for the test user
@pytest.fixture
def test_user():
    user = Users(
        username='test_user',
        email='test_user@example.com',
        first_name='Test',
        last_name='User',
        hashed_password=bcrypt_context.hash('test_password'),
        role='admin',
        phone_number='(123) 456-7890',
        is_active=True
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()