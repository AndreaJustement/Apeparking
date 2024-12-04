from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.auth_service import is_user

dashboard_router = APIRouter()
templates = Jinja2Templates(directory="app/templates/user")

# Ruta principal del dashboard
@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request, user: dict = Depends(is_user)):
    return templates.TemplateResponse("user_dashboard.html", {"request": request, "user": user})

# Ruta para el perfil del usuario
@dashboard_router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user: dict = Depends(is_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

# Ruta para el historial del usuario
@dashboard_router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse("user/history.html", {"request": request})
