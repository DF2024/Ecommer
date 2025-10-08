from typing import Optional
from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    stock: int
    image_path: Optional[str] = Field(default = None)


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass

class ProductResponse(Product):
    imagen_url: Optional[str] 
    pass

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None