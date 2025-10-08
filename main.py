import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.backend.config.db import lifespan
from app.backend.routers import users, users_frontend, product, product_frontend



app = FastAPI(
    lifespan = lifespan
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#CONFIGURAR RUTAS ESTATICAS 
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name = "static")


#CONFIGURAR PLANTILLAS
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

app.include_router(users.router)
app.include_router(users_frontend.router)
#app.include_router(product.router)
app.include_router(product_frontend.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("users/login.html", {"request": request, "title": "Inicio de Sesión"})

@app.get("/product", response_class=HTMLResponse)
async def product(request: Request):
    return templates.TemplateResponse("products/create.html", {"request": request, "title": "Lista de productos"})