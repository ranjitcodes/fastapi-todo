from sqlalchemy import Table, Column, Integer, String, MetaData
from .database import database

metadata = MetaData()

todo_table=Table(
    "todo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task", String, nullable=False)
)
