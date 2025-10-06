from fastapi import APIRouter, HTTPException, status
from backend.models.users import UserCreate, User, UserResponse, UserLogin, UserUpdate, Token
from sqlmodel import select, update, delete
from backend.config.db import SessionDep
from backend.auth import auth
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")


## CREAR USUARIO

@router.post('/users/register', response_model=UserResponse, tags=['Users'])
async def user_register(
    user_data: UserCreate,
    session: SessionDep,
):
    # Verifica también por email
    statement = select(User).where(
        (User.username == user_data.username) | 
        (User.email == user_data.email)
    )
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario o email ya existen")

    hashed_password = auth.hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Convierte el objeto User a UserResponse
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email
    )
## LOGEAR USUARIO

@router.post("/users/login", response_model = Token)
async def login_user(
    user_data : UserLogin , 
    session : SessionDep
):
    statament = select(User).where(User.username == user_data.username)
    db_user = session.exec(statament).first()

    if not db_user or not auth.verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = auth.create_access_tokken({"sub": db_user.username})

    return {"access_token" : token, "token_type" : "bearer"}


## REVISAR LISTA DE USUARIOS

@router.get("/users", response_model = list[User], tags = ['Users'])
async def user_get(session : SessionDep):
    statament = select(User)
    result = session.exec(statament)
    users = result.all()
    return users

## REVISAR UNICO USUARIO POR ID

@router.get("/users/{id_user}", response_model = User ,tags = ['Users'])
async def get_user_id(id_user : int, session : SessionDep):
    statament = select(User).where(User.id == id_user)
    user = session.exec(statament).first()
    return user

## BORRAR USUARIO POR ID

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

## ACTUALIZAR USUARIO POR ID

@router.patch("/users/{id_user}", tags = ['Users'])
async def update_user(id_user : int, user_data : UserUpdate, session : SessionDep):
    user_db = session.get(User, id_user)

    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Task doesn't exist"
    )

    update_data = user_data.dict(exclude_unset=True)

    if update_data:
        statement = update(User).where(User.id == id_user).values(**update_data)
        session.exec(statement)
        session.commit()
        user_db = session.get(User, id_user)
    
    return user_db