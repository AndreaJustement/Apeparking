from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Verificar contraseñas
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Crear hash de contraseñas
def get_password_hash(password):
    return pwd_context.hash(password)

# Crear token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Obtener usuario actual desde el token
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    if not token:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="No autenticado")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "cliente")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Verificar si el usuario es un cliente
async def is_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "cliente":
        raise HTTPException(status_code=403, detail="No tienes acceso a esta funcionalidad")
    return current_user

# Verificar si el usuario es administrador
async def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes acceso a esta funcionalidad")
    return current_user
