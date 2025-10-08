import os
from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.backend.config.db import SessionDep
from app.backend.models.product import Product
from app.backend.utils.file_utils import save_uploaded_file, delete_product_image, get_image_url

router = APIRouter(prefix = "/products", tags = ["Products Frontend"])

API_BASE_URL = "http://127.0.0.1:8000"

current_file_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_file_dir)
app_dir = os.path.dirname(backend_dir)
templates_dir = os.path.join(app_dir, "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
async def list_product(request : Request, session : SessionDep):
    products = session.exec(select(Product)).all()
    return templates.TemplateResponse("products/product_list.html", {"request" : request, "products" : products})

@router.get("/create", response_class = HTMLResponse)
async def create_form(request : Request):
    return templates.TemplateResponse("products/create.html", {"request" : request})

@router.post("/create", tags=["Products"])
async def create_product(
    request: Request,
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None)
):
    image_filename = None

    if image and image_filename:
        image_filename = save_uploaded_file(image)


    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_filename
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    # Redirige a la lista de productos (ajústala si aún no existe)
    return RedirectResponse(url="/products", status_code=303)


@router.get("/edit/{product_id}", response_class = HTMLResponse)
async def edit_form(product_id: int, request : Request, session : SessionDep):
    product = session.get(Product, product_id)
    if not product:
        return RedirectResponse("/products", status_code=303)
    return templates.TemplateResponse("products/edit.html", {"request": request, "product": product})

@router.post("/edit/{product_id}")
async def update_product(
    session: SessionDep,
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None),
):
    product = session.get(Product, product_id)
    if not product: 
        return RedirectResponse("/products", status_code=303)
    
    # Procesar nueva imagen si se subió
    if image and image.filename:
        # Eliminar imagen anterior si existe
        if product.image_path:
            delete_product_image(product.image_path)
        # Guardar nueva imagen
        image_filename = save_uploaded_file(image)
        product.image_path = image_filename

    # Actualizar otros campos
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    
    session.commit()
    return RedirectResponse("/products", status_code=303)


@router.get("/delete/{product_id}")
async def delete_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if product:
        if product.image_path:
            delete_product_image(product.image_path)
        session.delete(product)
        session.commit()
    return RedirectResponse("/products", status_code=303)