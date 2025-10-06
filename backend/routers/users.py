from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def ola():
    return {'messege' : 'Hola desde el router'}