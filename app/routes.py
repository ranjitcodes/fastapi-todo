from fastapi import APIRouter, HTTPException, Response, status, Depends
from .models import todo_table, users_table
from .database import database
from .schemas import Todo, TodoCreate, TodoUpdate, UserCreate, UserOut, UserLogin, Token
from .utils import hash_password, verify_password
from .jwt import create_access_token
from .auth import get_current_user

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Server is live"}

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@router.get("/protected_route")
async def protected(current_user:dict=Depends(get_current_user)):
    return {"message": "You are authenticated!", "user":current_user}


@router.get("/todos", response_model=list[Todo])
async def get_todos(current_user:dict=Depends(get_current_user)):
    query = todo_table.select().where(todo_table.c.user_id==current_user["user_id"])
    todos = await database.fetch_all(query)
    return todos


@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoCreate, current_user:dict=Depends(get_current_user)):
    query = todo_table.insert().values(task=todo.task, user_id=current_user["user_id"])
    todo_id = await database.execute(query)
    return {**todo.dict(), "id": todo_id, "user_id":current_user["user_id"]}


@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate, current_user:dict=Depends(get_current_user)):
    query = todo_table.select().where(todo_table.c.id == todo_id, todo_table.c.user_id==current_user["user_id"])
    is_existing = await database.fetch_one(query)
    if not is_existing:
        raise HTTPException(status_code=404, detail="Todo ID not found")

    update_query = (
        todo_table.update().where(todo_table.c.id == todo_id).values(task=todo.task)
    )
    await database.execute(update_query)
    return {**todo.dict(), "id": todo_id, "user_id":current_user["user_id"]}


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, current_user:dict=Depends(get_current_user)):
    query = todo_table.select().where(todo_table.c.id == todo_id, todo_table.c.user_id==current_user["user_id"])
    is_existing = await database.fetch_one(query)
    if not is_existing:
        raise HTTPException(status_code=404, detail="Todo ID not found.")

    delete_query = todo_table.delete().where(todo_table.c.id == todo_id)
    await database.execute(delete_query)
    return Response(status_code=204)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    user_role = "user"
    query = users_table.select().where(users_table.c.username == user.username)
    is_existing = await database.fetch_one(query)
    if is_existing:
        raise HTTPException(status_code=400, detail="Username Already Registered.")

    hashed_pw = hash_password(user.password)
    insert_query = users_table.insert().values(
        username=user.username, password=hashed_pw, role=user_role
    )
    user_id = await database.execute(insert_query)
    register_response = {"id": user_id, "username": user.username}
    return register_response


@router.post("/login", response_model=Token)
async def login_user(user: UserLogin):
    query = users_table.select().where(users_table.c.username == user.username)
    db_user = await database.fetch_one(query)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect Username or Password")

    token = create_access_token(
        {"user_id": db_user["id"], "username": db_user["username"], "role": db_user["role"]}
    )
    login_response = {"access_token": token, "token_type": "bearer"}
    return login_response
