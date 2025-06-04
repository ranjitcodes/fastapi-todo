from fastapi import APIRouter, HTTPException, Response
from .models import todo_table
from .database import database
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    task: str

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Server is live"}

@router.get("/todos")
async def get_todos():
    query = todo_table.select()
    return await database.fetch_all(query)

@router.post("/todos")
async def add_todo(todo: Todo):
    query = todo_table.insert().values(id=todo.id, task=todo.task)
    try:
        await database.execute(query)
    except:
        raise HTTPException(status_code=400, detail="Duplicate Todo ID or Insert Error.")           
    return todo
    
@router.put("/todos/{todo_id}")
async def update_todo(todo_id: int, updated_todo: Todo):
    query=todo_table.select().where(todo_table.c.id==todo_id)
    is_existing= await database.fetch_one(query)
    if not is_existing:
        raise HTTPException(status_code=404,detail="Todo ID not found.")
    
    update_query=todo_table.update().where(todo_table.c.id==todo_id).values(task=updated_todo.task)
    await database.execute(update_query)
    return updated_todo
    
    
@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    query=todo_table.select().where(todo_table.c.id==todo_id)
    is_existing= await database.fetch_one(query)
    if not is_existing:
        raise HTTPException(status_code=404,detail="Todo ID not found.")
    
    delete_query=todo_table.delete().where(todo_table.c.id==todo_id)
    await database.execute(delete_query)
    return Response(status_code=204)