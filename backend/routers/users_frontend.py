from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter(prefix="/frontend/users", tags=["Frontend Users"])

API_BASE_URL = "http://127.0.0.1:8000"

# --------------------------
# PÁGINA DE REGISTRO
# --------------------------

@router.get("/register", response_class = HTMLResponse)
async def register_page(request : Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Registro"})

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
            return RedirectResponse(url="/frontend/users/register", status_code=status.HTTP_303_SEE_OTHER)

# --------------------------
# PÁGINA DE LOGIN
# --------------------------

@router.get("/login", response_class = HTMLResponse)
async def login_page(request : Request):
    return templates.TemplateResponse("login.html", {"request" : request, "title": "Registro"})

@router.post("/login")
async def login_user(
    username : str = Form(...),
    password : str = Form(...)
):
    async with httpx.AsyncClient() as client:
        data = {"username": username, "password": password}
        response = await client.post(f"{API_BASE_URL}/users/login", json=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else: 
        return RedirectResponse(url="/frontend/users/login", status_code=status.HTTP_303_SEE_OTHER)