import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routes import router
from .admin_routes import router as admin_router
from .database import database

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

app = FastAPI(
    title="Todo API with JWT Auth",
    version="1.0.0",
    description="This is a secure Todo API using JWT token authentication",
    docs_url="/docs" if DEBUG else None,
    redoc_url=None,
    openapi_url="/openapi.json" if DEBUG else None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(admin_router)

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
