from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from bson import ObjectId
from app.core.config import settings
from app.db.mongodb import get_database
from pymongo.database import Database
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from app.core.config import USE_ADVANCED_SECURITY
# Configuración de OAuth2 para la autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener el usuario actual a partir del token JWT
async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_database)):
   if not USE_ADVANCED_SECURITY:  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Remover "Bearer " si está presente en el token
    if "Bearer " in token:
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "cliente")
        print(f"ID de usuario: {user_id}, Rol: {role}")

        if user_id is None:
            raise credentials_exception

        # Convierte el user_id en ObjectId y verifica si el usuario existe
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise credentials_exception
        
        # Agrega el rol al diccionario del usuario para futuras verificaciones
        user["rol"] = role
        return user
    except JWTError as e:
        print(f"Error de JWT: {e}")
        raise credentials_exception

async def is_user(user: dict = Depends(get_current_user)):
  if USE_ADVANCED_SECURITY:  
    if "rol" not in user or user["rol"] != "cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de usuario estándar"
        )
    return user

async def is_admin(user: dict = Depends(get_current_user)):
   if USE_ADVANCED_SECURITY: 
    if user.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return user

#register

async def register_user(user_data: dict, db: Database):
    await db["users"].insert_one(user_data)
