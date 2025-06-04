from fastapi import APIRouter, HTTPException, Response
from .models import Todo
from .data import todos

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Server is live"}

@router.get("/todos")
def get_todos():
    return todos

@router.post("/todos")
def add_todo(todo: Todo):
    for t in todos:
        if t["id"]==todo.id:
            raise HTTPException(status_code=400, detail="Duplicate Todo ID found")
    todos.append(todo.dict())
    return todo
    
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo["id"]==todo_id:
            todos[index]=updated_todo.dict()
            return updated_todo
    raise HTTPException(status_code=404,detail="Todo ID not found.")
    
@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"]==todo_id:
            todos.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Todo ID not found.")