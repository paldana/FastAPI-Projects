from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from models import Todos 
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user


router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db    # will execute the code up to this point, execute the queries in db, and then return the db session to the caller
    finally: 
        db.close()  # close the database connection every after a db request is made


db_dependency = Annotated[Session, Depends(get_db)]  # create a dependency for the db session
user_dependency = Annotated[dict, Depends(get_current_user)]  # create a dependency for the current user

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=200)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)



@router.get("/")
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="User Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()  # return all todos that belong to the current user


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0),):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()   # get the todo model from the database using the todo_id and the current user's id
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with the id {todo_id} is not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Authentication Failed")
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))  # create a new todo model using the request data and the current user's id   

    db.add(todo_model)
    db.commit()
    return {"message": "Todo created successfully."}


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0), todo_request: TodoRequest = None):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()   # get the todo model from the database using the todo_id and the current user's id

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with the id {todo_id} is not found under the current user")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    return {"message": "Todo updated successfully."}


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()   # get the todo model from the database using the todo_id and the current user's id

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with the id {todo_id} is not found under the current user")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return {"message": "Todo deleted successfully."}