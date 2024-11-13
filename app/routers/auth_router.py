from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from app.db.mongodb import get_database
from pymongo.database import Database
from jose import jwt
from app.core.config import settings, USE_ADVANCED_SECURITY
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from bson import ObjectId
from app.services.auth_service import is_user, is_admin, get_current_user
from fastapi.responses import HTMLResponse
templates = Jinja2Templates(directory="app/templates")
auth_router = APIRouter()

# Función para crear el token de acceso
def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Endpoint para mostrar el formulario de login
@auth_router.get("/login")
async def show_login(request: Request):
    print("Mostrando formulario de login")
    return templates.TemplateResponse("login.html", {"request": request})

# Endpoint para procesar el login con redirección según el rol
@auth_router.post("/login")
async def process_login(
    request: Request,
    email: EmailStr = Form(...),
    contrasena: str = Form(...),
    db: Database = Depends(get_database)
):
    print(f"Intento de login para: {email}")
    # Buscar al usuario en la base de datos
    user = await db["users"].find_one({"email": email})
    if not user or not bcrypt.checkpw(contrasena.encode("utf-8"), user["contrasena"].encode("utf-8")):
        print("Credenciales incorrectas o usuario no encontrado")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})
    
    # Determinar la URL de redirección basada en el rol
    if user.get("rol") == "admin":
        redirect_url = "/admin/dashboard"
    else:
        redirect_url = "/dashboard"

    # Configurar la respuesta de redirección
    response = RedirectResponse(url=redirect_url, status_code=303)

    # Si USE_ADVANCED_SECURITY está activo, genera y añade el token a la cookie
    if USE_ADVANCED_SECURITY:
        token_data = {"sub": str(user["_id"]), "role": user.get("rol", "cliente")}
        access_token = create_access_token(data=token_data)
        print(f"Token generado: {access_token}")
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="Lax")
    else:
        # En modo básico, añade una cookie simple sin token
        response.set_cookie(key="basic_auth", value="authenticated", httponly=True, samesite="Lax")

    print(f"Redirigiendo a: {redirect_url}")
    return response

# Endpoint para obtener el token (uso en Swagger UI o autenticación por API)
@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Database = Depends(get_database)
):
    if not USE_ADVANCED_SECURITY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token endpoint no disponible en modo básico")

    print(f"Intento de obtención de token para: {form_data.username}")
    # Buscar al usuario en la base de datos
    user = await db["users"].find_one({"email": form_data.username})
    
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user["contrasena"].encode('utf-8')):
        print("Credenciales incorrectas en token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear el token de acceso
    token_data = {"sub": str(user["_id"]), "role": user.get("rol", "cliente")}
    access_token = create_access_token(data=token_data)
    print(f"Token generado para Swagger UI: {access_token}")
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para mostrar el formulario de registro
@auth_router.get("/register")
async def show_register(request: Request):
    print("Mostrando formulario de registro")
    return templates.TemplateResponse("register.html", {"request": request})

# Endpoint para procesar el registro de un nuevo usuario
@auth_router.post("/register")
async def register_user_endpoint(
    request: Request,
    email: EmailStr = Form(...),
    contrasena: str = Form(...),
    nombre: str = Form(...),
    db: Database = Depends(get_database)
):
    print(f"Intento de registro para: {email}")
    # Verifica si el usuario ya existe
    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        print("Usuario ya existe en la base de datos")
        return templates.TemplateResponse("register.html", {"request": request, "error": "El usuario ya existe"})

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_data = {"email": email, "contrasena": hashed_password, "nombre": nombre, "rol": "cliente"}

    # Insertar el usuario en la base de datos
    await db["users"].insert_one(user_data)
    print("Usuario registrado exitosamente")
    
    # Redirigir al login después del registro exitoso
    return RedirectResponse(url="/login", status_code=303)

