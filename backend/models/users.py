from sqlmodel import SQLModel, Field 
from datetime import datetime
from pydantic import EmailStr
from typing import Optional

class User(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    username : str = Field(default = None)
    email : EmailStr = Field(default = None)
    hashed_password : str
    created_at : datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    username : str
    email : EmailStr
    password : str

class UserLogin(SQLModel):
    username : str
    password : str

class UserUpdate(SQLModel):
    username : str
    email : str

class Token(SQLModel):
    access_token: str
    token_type: str

class UserResponse(SQLModel):
    id: int
    username: str
    email: EmailStr