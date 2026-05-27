from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

class TodoUpdate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

todos = []
next_id = 1

# Helper function for finding todo:
def find_todo(todo_id: int) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
        
    raise HTTPException(status_code=404, detail="TODO not found!")

@app.get("/todos")
async def get_todos(skip: int = 0, limit: int = 4, is_checked: bool | None = None):
    if is_checked is not None:
        return [todo for todo in todos if todo["is_completed"] == is_checked]
    
    return todos[skip: skip + limit]

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    
    todo = find_todo(todo_id)
    
    if todo:
        return todo

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

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate):
    result = find_todo(todo_id)

    if result:
        result["title"] = todo.title
        result["description"] = todo.description
        result["is_completed"] = todo.is_completed

    return result

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    todo = find_todo(todo_id)

    if todo:
        todos.remove(todo)


