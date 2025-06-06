from pydantic import BaseModel, constr
from typing import Optional
# Todo Schemas

class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass 

class TodoUpdate(TodoBase):
    pass 

class TodoInDBBase(TodoBase):
    id: int
    user_id: int 
    
    class Config:
        orm_mode = True

class Todo(TodoInDBBase):
    pass 


# User Schemas

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    
class UserCreate(UserBase):
    password: constr(min_length=6)
    role: Optional[str]="user"
    
class UserOut(UserBase):
    id: int
    
    class Config:
        orm_mode: True
        
class UserLogin(BaseModel):
    username: str
    password: str


# JWT Token Schema

class Token(BaseModel):
    access_token: str
    token_type: str