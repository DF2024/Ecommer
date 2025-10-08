from fastapi import APIRouter, HTTPException, status
from app.backend.models.product import Product, ProductResponse, ProductCreate, ProductUpdate
from sqlmodel import select, update, delete
from app.backend.config.db import SessionDep

router = APIRouter()

##CREAR PRODUCTOS
@router.post("/products/create", response_model = ProductResponse, tags = ['Products'])
async def product_create(
    product_data : ProductCreate,
    session : SessionDep
):
    
    statament = select(Product).where(
        (Product.name == product_data.name)
    )

    existing_product = session.exec(statament).first()

    if existing_product:
        raise HTTPException(status_code = 400, detail = "Producto ya existe")
    
    new_product = Product(
        name = product_data.name,
        description = product_data.description,
        price = product_data.price,
        stock = product_data.stock,
        img = product_data.image_url   
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product

## LISTAR PRODUCTOS
@router.get("/products/list", response_model = list[Product], tags = ['Products'])
async def product_get(session : SessionDep):
    statament = select(Product)
    result = session.exec(statament)
    products = result.all()
    return products

## REVISAR UNICO PRODUCTO POR ID 

@router.get("/products/{id_product}", response_model = Product ,tags = ['Products'])
async def get_product_id(
    id_product : int,
    session : SessionDep
    ):
    statament = select(Product).where(Product.id == id_product)
    product = session.exec(statament).first()
    return product

## BORRAR USUARIO POR ID

@router.delete("/product/{id_product}", tags = ['Products'])
async def delete_user(id_product : int, session : SessionDep):
    product_db = session.get(Product, id_product)


    if not product_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Task doesn't exist"
        )
    
    session.delete(product_db)
    session.commit()
    return {'message': 'Task deleted successfully', 
            'deleted_task': product_db.dict()} 

## ACTUALIZAR USUARIO POR ID

@router.patch("/product/{id_product}", tags = ['Products'])
async def update_user(id_product : int, product_data : ProductUpdate, session : SessionDep):
    product_db = session.get(Product, id_product)

    if not product_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Task doesn't exist"
    )

    update_data = product_data.dict(exclude_unset=True)

    if update_data:
        statement = update(Product).where(Product.id == id_product).values(**update_data)
        session.exec(statement)
        session.commit()
        product_db = session.get(Product, id_product)
    
    return product_db