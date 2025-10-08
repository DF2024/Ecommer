import os
import uuid
from fastapi import UploadFile, HTTPException
from typing import Optional

class FileManager:
    def __init__(self, upload_subdirectory: str):
        # Obtener la ruta absoluta del directorio del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        project_root = os.path.dirname(backend_dir)
        
        self.upload_directory = os.path.join(
            project_root, 
            "frontend", 
            "static", 
            "uploads", 
            upload_subdirectory
        )
        
        # Crear directorio si no existe
        os.makedirs(self.upload_directory, exist_ok=True)
        print(f"📁 Directorio de uploads: {self.upload_directory}")  # Para debug
    
    def save_uploaded_file(self, upload_file: UploadFile) -> str:
        """Guarda un archivo subido y retorna el nombre del archivo guardado"""
        if not upload_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Validar tamaño (5MB máximo)
        file_content = upload_file.file.read()
        file_size = len(file_content)
        if file_size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400, 
                detail="La imagen es demasiado grande. Máximo 5MB"
            )
        
        # Generar nombre único
        file_extension = os.path.splitext(upload_file.filename)[1].lower()
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_directory, filename)
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        print(f"💾 Imagen guardada: {filename}")  # Para debug
        return filename
    
    def delete_file(self, filename: str) -> bool:
        """Elimina un archivo y retorna si fue exitoso"""
        if not filename:
            return False
            
        file_path = os.path.join(self.upload_directory, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Imagen eliminada: {filename}")  # Para debug
                return True
            except OSError as e:
                print(f"❌ Error eliminando imagen: {e}")
                return False
        return False
    
    def file_exists(self, filename: str) -> bool:
        """Verifica si un archivo existe"""
        if not filename:
            return False
        file_path = os.path.join(self.upload_directory, filename)
        return os.path.exists(file_path)

# Instancias globales para usar en toda la app
product_file_manager = FileManager("products")
user_file_manager = FileManager("users")