from sqlalchemy import Table, Column, Integer, String, MetaData
from .database import database

metadata = MetaData()

todo_table=Table(
    "todo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task", String, nullable=False),
    Column("user_id", Integer, nullable=False)
)

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("password", String, nullable=False),
    Column("role", String, default="user")
)