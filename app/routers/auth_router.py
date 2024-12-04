from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm  # Importa aquí
from datetime import timedelta
from app.db.mongodb import get_database
from app.services.auth_service import create_access_token, verify_password
from pymongo.database import Database

auth_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@auth_router.get("/login", response_model=None)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_database)):
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # Generar token de acceso
    access_token_expires = timedelta(minutes=60)
    token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=access_token_expires)

    # Redirigir según el rol del usuario
    redirect_url = "/admin/dashboard" if user.get("role") == "admin" else "/dashboard"
    response = RedirectResponse(url=redirect_url, status_code=303)

    # Configurar cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="Strict",
        secure=False,  # Cambia a True si usas HTTPS
    )
    return response


@auth_router.get("/logout", response_model=None)
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
