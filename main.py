import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID
from model import *
from mangum import Mangum

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="Todo-service")
# use when deploying with serverless as a parameter
# openapi_prefix=openapi_prefix

class Todo(BaseModel):
    pk:str
    id: str
    title: str
    notes: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "id": "4baf6eaf-a1dd-4540-8c0a-db65798ee746",
                "title": "title",
                "notes": "notes",
                "status": "In progress",
            }
        }


TODOS = [] # aab48765-83be-41b3-a085-9a0d97726303

# list all the todos
@app.get("/todos")
def list_todos():
    # create a response
    response = pynamo_list_all()
    return response


# get a todo by id -- working
@app.get("/todo/{id}")
def get_todo(id: str):
    try:
        # query for todo
        response = pynamo_get_one(id)
        return response
    except:
        response = {
            "status": 404,
            "message": "Todo not found"
        }
        return response


# update a todo by id
@app.put("/todo/{id}")
def update_todo(id: str, todo_title: str, todo_notes: str, todo_status: str):
    # use the parameters and create and updated todo
    updated_todo = {
        "id": id,
        "title": todo_title,
        "notes": todo_notes,
        "status": todo_status
    }
    try:
        response = pynamo_update(updated_todo)
        return response
    except:
        response = {
            "status": 404,
            "message": "Todo not found"
        }
        return response


# delete a todo by id
@app.delete("/todo/{id}")
def delete_todo(id: str):
    try:
        # delete the todo by id
        response = pynamo_delete(id)
        return response
    except:
        response = {
            "status": 404,
            "message": "Todo not found"
        }
        return response



# create a new todo
@app.post("/todo")
def create_todo(title: str):
    new_todo = {
        "title": title
    }
    # add new todo to dynamoDB
    response = pynamo_create(new_todo)

    return response


# seed our fake db TODOS for testing purposes
def seed():
    todo1 = {
        "id": "1baf6eaf-a1dd-4540-8c0a-db65798ee746",
        "title": "task 1",
        "notes": "No notes",
        "status": "In progress"
    }
    todo2 = {
        "id": "2baf6eaf-a1dd-4540-8c0a-db65798ee746",
        "title": "task 2",
        "notes": "No notes",
        "status": "In progress"
    }
    todo3 = {
        "id": "3baf6eaf-a1dd-4540-8c0a-db65798ee746",
        "title": "task 3",
        "notes": "No notes",
        "status": "In progress"
    }

    # commit to TODOS DB
    TODOS.append(todo1)
    TODOS.append(todo2)
    TODOS.append(todo3)

handler = Mangum(app)
