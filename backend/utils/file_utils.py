import os 
import uuid
from fastapi import UploadFile, HTTPException
from typing import Optional

current_file_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_file_dir)
app_dir = os.path.dirname(backend_dir)
UPLOAD_DIRECTORY = os.path.join(app_dir, "frontend", "static", "uploads", "products")

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def save_uploaded_file(upload_file: UploadFile) -> str:
    """Guarda un archivo subido y retorna el nombre del archivo guardado"""
    if not upload_file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # Validar tamaño del archivo (opcional - 5MB máximo)
    file_content = upload_file.file.read()
    if len(file_content) > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="La imagen es demasiado grande. Máximo 5MB")
    
    # Generar nombre único
    file_extension = os.path.splitext(upload_file.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    # Guardar el archivo
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    return filename

def delete_product_image(image_path: str) -> bool:
    """Elimina la imagen de un producto y retorna si fue exitoso"""
    if image_path:
        file_path = os.path.join(UPLOAD_DIRECTORY, image_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except OSError:
                return False
    return False

def get_image_url(image_path: Optional[str]) -> Optional[str]:
    """Genera la URL completa para acceder a la imagen"""
    if image_path:
        return f"/static/uploads/products/{image_path}"
    return None

def get_image_path(image_url: Optional[str]) -> Optional[str]:
    """Extrae el nombre del archivo desde una URL"""
    if image_url:
        return os.path.basename(image_url)
    return None

def is_valid_image_file(file: UploadFile) -> bool:
    """Valida si el archivo es una imagen válida"""
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
    return file.content_type in allowed_types

def get_allowed_extensions() -> list:
    """Retorna las extensiones permitidas"""
    return ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']

