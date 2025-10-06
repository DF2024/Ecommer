from fastapi import FastAPI
from routers import users
from config.db import lifespan

app = FastAPI(
    lifespan = lifespan
)

app.include_router(users.router)

