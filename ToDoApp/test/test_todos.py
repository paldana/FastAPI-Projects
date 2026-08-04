from ..routers.todos import get_db, get_current_user
# from ..models import Todos
from .utils import *
from fastapi import status

# Set the dependency overrides for the FastAPI app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todo/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Check if the response is a list 
    assert response.json() == [{'title': 'Test Todo', 
                                'description': 'This is a test todo', 
                                'priority': 1, 
                                'complete': False, 
                                'owner_id': 1, 
                                'id': 1}]  # Check if the response contains the test todo    


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)  # Check if the response is a dictionary
    assert response.json() == {'title': 'Test Todo', 
                                'description': 'This is a test todo', 
                                'priority': 1, 
                                'complete': False, 
                                'owner_id': 1, 
                                'id': 1} # Check if the response contains the test todo    

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")  # Use a non-existent todo_id
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with the id 999 is not found"}  # Check if the response contains the correct error message


def test_create_todo(test_todo):
    request_data = {
        "title": "New Test Todo",
        "description": "This is a new test todo",
        "priority": 2,
        "complete": False
    }
    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Todo created successfully."}  # Check if the response contains the correct success message

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()    # id == 2 because the first test_todo has id == 1 from the fixture
    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]


def test_update_todo(test_todo):
    request_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo",
        "priority": 3,
        "complete": True
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo",
        "priority": 3,
        "complete": True
    }
    response = client.put("/todo/999", json=request_data)  # Use a non-existent todo_id
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with the id 999 is not found under the current user"}  # Check if the response contains the correct error message


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None  # Check if the todo has been deleted from the database

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")  # Use a non-existent todo_id
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with the id 999 is not found under the current user"}  # Check if the response contains the correct error message
