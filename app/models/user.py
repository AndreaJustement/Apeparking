from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: str
    nombre: str
    contrasena: str
    rol: str = "cliente"  # Por defecto cliente, pero puede ser 'admin'

    class Config:
        json_encoders = {
            ObjectId: str
        }
