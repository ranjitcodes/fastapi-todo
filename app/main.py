from fastapi import FastAPI
from .routes import router
from .database import database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.on_event("startup")
async def connect():
    await database.connect()
    
@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()
 