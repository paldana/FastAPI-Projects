from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status

# Set the dependency overrides for the FastAPI app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Check if the response is a list
    assert response.json() == [{'title': 'Test Todo', 
                                    'description': 'This is a test todo', 
                                    'priority': 1, 
                                    'complete': False, 
                                    'owner_id': 1, 
                                    'id': 1}]  # Check if the response contains the test todo    

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()  # Check if the todo with id 1 has been deleted
    assert model is None  # The model should be None if it was successfully deleted

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")  # Use a non-existent todo_id
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with the id 999 is not found"}  # Check if the response contains the correct error message