from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

todos = []
next_id = 1

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

# Helper function for finding todo:
def find_todo(todo_id: int) -> dict | None:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
        
    return None

@app.get("/todos")
async def get_todos(
    skip: int = 0, 
    limit: int = 4, 
    checked: bool | None = None
):
    result = todos
    
    if checked is not None:
        return [todo for todo in result if todo["completed"] == checked]
    
    return result[skip: skip + limit]


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    
    todo = find_todo(todo_id)
    
    if not todo:
        raise HTTPException(status_code=404, detail="TODO not found!")
    
    return todo

@app.post("/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    global next_id

    new_todo = {
        "id": next_id,
        **todo.model_dump()
    }

    todos.append(new_todo)
    next_id += 1

    return new_todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate):
    result = find_todo(todo_id)

    if not result:
        raise HTTPException(status_code=404, detail="TODO not found!")

    result["title"] = todo.title
    result["description"] = todo.description
    result["completed"] = todo.completed

    return result

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="TODO not found!")    
    
    todos.remove(todo)


