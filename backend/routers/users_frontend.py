import os
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter(prefix="/frontend/users", tags=["Frontend Users"])

API_BASE_URL = "http://127.0.0.1:8000"

# --- NUEVA CONFIGURACIÓN DE PLANTILLAS PARA ESTE ROUTER ---
# Obtener el directorio base de la aplicación de forma robusta
# Para este archivo (users_frontend.py) su propio BASE_DIR es app/backend/routers
# Necesitamos subir dos niveles para llegar a la carpeta 'app'
# y luego acceder a 'frontend/templates'
current_file_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel de 'routers' a 'backend'
backend_dir = os.path.dirname(current_file_dir)
# Subimos un nivel de 'backend' a 'app'
app_dir = os.path.dirname(backend_dir)
# Ahora podemos construir la ruta a las plantillas
templates_dir = os.path.join(app_dir, "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)
# ----------------------------------------------------------

# --------------------------
# PÁGINA DE REGISTRO
# --------------------------

@router.get("/register", response_class = HTMLResponse)
async def register_page(request : Request):
    return templates.TemplateResponse("users/register.html", {"request": request, "title": "Registro"})

@router.post("/register")
async def register_user(
    username : str = Form(...),
    email : str = Form(...),
    password: str = Form(...)
):
    async with httpx.AsyncClient() as client:
        data = {"username": username, "email": email, "password": password}
        response = await client.post(f"{API_BASE_URL}/users/register", json=data)

        if response.status_code == 200:
            return RedirectResponse(url="/frontend/users/login", status_code=status.HTTP_303_SEE_OTHER)
        else:
            # Considera pasar un mensaje de error a la plantilla aquí
            return RedirectResponse(url="/frontend/users/register", status_code=status.HTTP_303_SEE_OTHER)

# --------------------------
# PÁGINA DE LOGIN
# --------------------------

@router.get("/login", response_class = HTMLResponse)
async def login_page(request : Request):
    # Asegúrate de que esta plantilla sea "login.html" si es lo que quieres para la página de login
    return templates.TemplateResponse("users/login.html", {"request" : request, "title": "Inicio de Sesión"})

@router.post("/login")
async def login_user(
    username : str = Form(...),
    password : str = Form(...)
):
    async with httpx.AsyncClient() as client:
        data = {"username": username, "password": password}
        response = await client.post(f"{API_BASE_URL}/users/login", json=data)

    if response.status_code == 200:
        # Aquí deberías manejar el token (guardarlo en una cookie, por ejemplo)
        # Por ahora, solo redirigimos
        token = response.json().get("access_token") # Aunque no se usa directamente aquí
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else: 
        # Considera pasar un mensaje de error a la plantilla aquí
        return RedirectResponse(url="/frontend/users/login", status_code=status.HTTP_303_SEE_OTHER)