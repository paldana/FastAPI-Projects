from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

# Set the dependency overrides for the FastAPI app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    ## we can verify the hashed password, but it will be different each time because of the salt, so we will not check it here
    # assert response.json()['hashed_password'] == test_user.hashed_password    
    assert response.json()['role'] == test_user.role
    assert response.json()['phone_number'] == test_user.phone_number
    assert response.json()['is_active'] == test_user.is_active
    assert response.json()['id'] == 1


def test_change_password_success(test_user):
    new_password = "new_test_password"
    response = client.put("/users/update-password", json={"current_password": "test_password", "new_password": new_password})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the password was changed in the database
    db = TestingSessionLocal()
    user_in_db = db.query(Users).filter(Users.username == test_user.username).first()
    assert bcrypt_context.verify(new_password, user_in_db.hashed_password)


def test_change_password_failure(test_user):
    response = client.put("/users/update-password", json={"current_password": "wrong_current_password", "new_password": "new_test_password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on Password Verification. Please check your password and try again."}

def test_change_password_user_not_found():
    # Override the get_current_user dependency to return a non-existent user
    def override_get_current_user_not_found():
        return {'username': 'non_existent_user', 'id': 999, 'role': 'admin'}

    app.dependency_overrides[get_current_user] = override_get_current_user_not_found

    response = client.put("/users/update-password", json={"current_password": "test_password", "new_password": "new_test_password"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User with the id 999 is not found"}

    # Reset the dependency override for get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user


def test_update_phone_number_success(test_user):
    new_phone_number = "(987) 654-3210"
    response = client.put("/users/update-phone-number", params={"new_phone_number": new_phone_number})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the phone number was changed in the database
    db = TestingSessionLocal()
    user_in_db = db.query(Users).filter(Users.username == test_user.username).first()
    assert user_in_db.phone_number == new_phone_number