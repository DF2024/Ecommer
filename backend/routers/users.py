from fastapi import APIRouter, HTTPException, status
from models.users import UserCreate, User, UserResponse, UserLogin
from sqlmodel import select, update, delete
from config.db import SessionDep
from auth import auth

router = APIRouter()

@router.post('/users/register', response_model = UserResponse, tags = ['Users'])
async def user_register(
    user_data : UserCreate,
    session : SessionDep,
):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Usuarion Existente")

    hashed_password = auth.hash_password(user_data.password)

    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message" : "Usuario Registrado con exito!"}

@router.get("/users", response_model = list[User], tags = ['Users'])
async def user_get(session : SessionDep):
    statament = select(User)
    result = session.exec(statament)
    users = result.all()
    return users

@router.get("/users/{id_user}", response_model = User ,tags = ['Users'])
async def get_user_id(id_user : int, session : SessionDep):
    statament = select(User).where(User.id == id_user)
    user = session.exec(statament).first()
    return user

@router.delete("/users/{id_user}", tags = ['Users'])
async def delete_user(id_user : int, session : SessionDep):
    user_db = session.get(User, id_user)


    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Task doesn't exist"
        )
    
    session.delete(user_db)
    session.commit()
    return {'message': 'Task deleted successfully', 
            'deleted_task': user_db.dict()} 