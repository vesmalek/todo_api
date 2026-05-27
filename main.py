from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

todos = []
next_id = 1

@app.get("/todos")
async def get_todos(skip: int = 0, limit: int = 2, is_checked: bool | None = None):
    return todos[skip: skip + limit]

@app.post("/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    global next_id
    id = next_id
    next_id = next_id + 1

    todo = {
        "id": id,
        **todo.model_dump()
    }

    todos.append(todo)

    return todo


