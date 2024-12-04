from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")  # MongoDB usa _id
    email: EmailStr  # Email válido
    nombre: str  # Nombre del usuario
    contrasena: str  # Contraseña sin encriptar por ahora
    rol: str = "cliente"  # Rol predeterminado

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "cliente@example.com",
                "nombre": "Juan Pérez",
                "contrasena": "123456",
                "rol": "cliente"
            }
        }
