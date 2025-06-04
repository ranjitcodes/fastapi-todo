from fastapi import FastAPI
from .routes import router
from .database import database

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def connect():
    await database.connect()
    
@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()
 