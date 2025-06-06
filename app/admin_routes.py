from fastapi import APIRouter, HTTPException, status, Depends
from .models import todo_table, users_table
from .database import database
from .schemas import Todo, TodoCreate, TodoUpdate, UserCreate, UserOut, UserLogin, Token
from .auth import get_current_user, get_current_admin
from sqlalchemy import select, func

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/todos", response_model=list[Todo], dependencies=[Depends(get_current_admin)])
async def get_all_todos():
    query=todo_table.select()
    todos=await database.fetch_all(query)
    return todos

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
async def delete_todo_admin(todo_id: int):
    query=todo_table.select().where(todo_table.c.id==todo_id)
    todo=await database.fetch_one(query)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")
    delete_query=todo_table.delete().where(todo_table.c.id==todo_id)
    await database.execute(delete_query)

@router.get("/users", response_model=list[UserOut], dependencies=[Depends(get_current_admin)])
async def get_users():
    query=users_table.select()
    users=await database.fetch_all(query)
    return users
    
@router.get("/users/{user_id}", response_model=UserOut, dependencies=[Depends(get_current_admin)])
async def get_user(user_id: int):
    query=users_table.select().where(users_table.c.id==user_id)
    user=await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
async def delete_user(user_id: int):
    query=users_table.select().where(users_table.c.id==user_id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    delete_query=users_table.delete().where(users_table.c.id==user_id)
    await database.execute(delete_query)
    
@router.get("/users/{user_id}/todos", response_model=list[Todo], dependencies=[Depends(get_current_admin)])
async def get_user_todos(user_id: int):
    query=todo_table.select().where(todo_table.c.user_id==user_id)
    todos=await database.fetch_all(query)
    return todos



@router.get("/stats", dependencies=[Depends(get_current_admin)])
async def get_admin_stats():
    user_count_query = select(func.count()).select_from(users_table)
    todo_count_query = select(func.count()).select_from(todo_table)

    total_users = await database.fetch_val(user_count_query)
    total_todos = await database.fetch_val(todo_count_query)

    return {"total_users": total_users, "total_todos": total_todos}


