from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pydantic import BaseModel
import uuid

def generate_id():
    return str(uuid.uuid4())

class Todo(Model):
    """
    TODO TABLE
    """
    class Meta:
        table_name = 'todo'
    pk = UnicodeAttribute(hash_key=True, default="TODO")
    id = UnicodeAttribute(range_key=True, default=generate_id())
    title = UnicodeAttribute(null=False)
    notes = UnicodeAttribute(default="No notes at this time")
    status = UnicodeAttribute(default="In progress")



# if table does not exist create it
if not Todo.exists():
        Todo.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


# Todo.delete_table()

# list all todos
def pynamo_list_all():
    # get all todos
    all_todos = Todo.query("TODO")
    # create a response
    response = {
        "status": 200,
        "message": f"Retrieving all todos",
        "todos": all_todos
    }

    return response

# get a todo
def pynamo_get_one(id):
    # query for todo
    todo = Todo.get("TODO", id)

    # create a response
    response = {
        "status": 200,
        "message": f"Task {todo.id} found",
        "Task": todo
    }

    return response

# updatae a todo
def pynamo_update(updated_todo):
    # get todo for updateing by id
    todo = Todo.get("TODO", updated_todo["id"])

    # update the todo with the updated_todo values
    todo.update(actions=[
        Todo.title.set(updated_todo["title"]),
        Todo.notes.set(updated_todo["notes"]),
        Todo.status.set(updated_todo["status"])
    ])

    # create a response
    response = {
        "status": 200,
        "message": f"Task {todo.id} updated",
        "body": todo
    }

    return response

# delete_todo
def pynamo_delete(id):
    # get todo for deletion by id
    todo = Todo.get("TODO", id)

    # delete the todo
    todo.delete()

    #create a response
    # create a response
    response = {
        "status": 200,
        "message": f"Task {todo.id} deleted",
    }

    return response

# create a todo
def pynamo_create(todo):
    # create a new todo dict
    new_todo = Todo(
        title=todo["title"],
    )
    # save to table
    new_todo.save()

    # return status code, creation messgae, and data that was saved
    return {
        "status": 200,
        "message": "New task created",
        "task": new_todo
    }
