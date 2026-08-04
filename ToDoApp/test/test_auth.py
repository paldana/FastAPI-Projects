from .utils import *
from ..routers.auth import authenticate_user, get_db, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
from datetime import timedelta
from jose import jwt, JWTError
from fastapi import status, HTTPException
import pytest

# Set the dependency overrides for the FastAPI app
app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user_success(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "test_password", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

def test_authenticate_user_non_existent_user():
    db = TestingSessionLocal()
    authenticated_user = authenticate_user("non_existent_user", "wrong_password", db)
    assert authenticated_user is False

def test_authenticate_user_wrong_password(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "wrong_password", db)
    assert authenticated_user is False


def test_create_access_token():
    username = 'test_user'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username=username, user_id=user_id, role=role, expires_delta=expires_delta)

    # Decode the token to verify its contents
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})
    assert decoded_token["sub"] == "test_user"
    assert decoded_token["id"] == 1
    assert decoded_token["role"] == "user"

## Works fine
def test_get_current_user_valid_token():
    encode = {'sub': 'test_user', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = get_current_user(token=token)
    assert user == {'username': 'test_user', 'id': 1, 'role': 'admin'}


## Throwing an error - TypeError: 'dict' object can't be awaited -- perhaps because get_current_user is not an async function, so it cannot be awaited.
# @pytest.mark.asyncio
# async def test_get_current_user_valid_token():
#     encode = {'sub': 'test_user', 'id': 1, 'role': 'admin'}
#     token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#     user = await get_current_user(token=token)     # --> TypeError: 'dict' object can't be awaited
#     assert user == {'username': 'test_user', 'id': 1, 'role': 'admin'}

def test_get_current_user_missing_payload():
    encode = {'sub': 'test_user', 'id': 1}  # Missing 'role' field
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token)
        
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"