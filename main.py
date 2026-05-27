from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

todos = []
next_id = 1

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


