from sqlmodel import SQLModel, Field, Optional 
from pydantic import EmailStr


class UserBase(SQLModel):
    username : str = Field(Default= None)
    email : EmailStr = Field(Defualt = None)
    hashed_password : str
    age : int
    
class User(UserBase, table = True):
    id : int = Optional[Field(default = None, primary_key = True)]

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    pass