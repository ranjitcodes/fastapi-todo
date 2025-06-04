"""
Run this script once to create database tables.
Do NOT import or run automatically in production or main app.
"""

from sqlalchemy import create_engine
from app.models import metadata
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please set it in your .env file.")

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

print("[+] Tables Created.")
