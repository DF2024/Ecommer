from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.config.db import lifespan
from backend.routers import users



app = FastAPI(
    lifespan = lifespan
)

#CONFIGURAR RUTAS ESTATICAS 
app.mount("/static", StaticFiles(directory="frontend/static"), name = "static")


#CONFIGURAR PLANTILLAS
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(users.router)

