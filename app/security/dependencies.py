from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from bson import ObjectId
from app.core.config import settings
from app.models.user import User
from app.db.mongodb import get_database
from fastapi.security import OAuth2PasswordBearer
from pymongo.database import Database
from app.services.auth_service import get_current_user
from core.config import USE_ADVANCED_SECURITY
# Configura OAuth2 para la autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener el usuario actual a partir del token JWT

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Database = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Intenta obtener el token de la cookie si no está en el header
    if not token:
        print("Token no encontrado en el header, intentando obtener de la cookie...")
        token = request.cookies.get("access_token")

    # Imprime el token para verificar si fue obtenido correctamente
    print(f"Token obtenido antes de procesar: {token}")

    if not token:
        print("No se encontró un token válido ni en el header ni en la cookie.")
        raise credentials_exception

    try:
        # Remueve "Bearer " si está presente
        if token.startswith("Bearer "):
            token = token[7:]

        # Imprime el token después de remover "Bearer "
        print(f"Token después de eliminar prefijo 'Bearer': {token}")

        # Decodifica el token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "cliente")
        
        # Imprime el contenido del payload para verificar el ID del usuario y el rol
        print(f"Payload decodificado: ID de usuario = {user_id}, Rol = {role}")

        if user_id is None:
            print("El ID de usuario no está presente en el token.")
            raise credentials_exception

        # Busca al usuario en la base de datos y verifica su existencia
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user is None:
            print("Usuario no encontrado en la base de datos.")
            raise credentials_exception
        
        # Agrega el rol al usuario y devuelve el usuario
        user["rol"] = role
        print("Usuario autenticado correctamente:", user)
        return user
    except JWTError as e:
        print(f"Error de JWT: {e}")
        raise credentials_exception





# Función para verificar si el usuario es estándar
async def is_user(user: dict = Depends(get_current_user)):
    print("Ejecutando is_user")
    if "rol" not in user or user["rol"] != "cliente":
        print("Acceso denegado en is_user")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de usuario estándar"
        )
    return user

async def is_admin(user: dict = Depends(get_current_user)):
    print("Ejecutando is_admin")
    if "rol" not in user or user["rol"] != "admin":
        print("Acceso denegado en is_admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return user
