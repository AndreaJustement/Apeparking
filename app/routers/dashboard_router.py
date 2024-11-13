from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.auth_service import is_user, get_current_user
from app.core.config import USE_ADVANCED_SECURITY

dashboard_router = APIRouter()
templates = Jinja2Templates(directory="app/templates/user")

# Ruta para el dashboard del usuario
@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request, user=Depends(is_user) if USE_ADVANCED_SECURITY else None):
    return templates.TemplateResponse("user_dashboard.html", {"request": request})

# Ruta para el perfil del usuario
@dashboard_router.get("/profile", name="dashboard_router.profile")
async def profile_page(request: Request, current_user=Depends(get_current_user) if USE_ADVANCED_SECURITY else None):
    return templates.TemplateResponse("user/profile.html", {"request": request, "user": current_user})

# Ruta para el historial del usuario
@dashboard_router.get("/history", name="dashboard_router.history")
async def history_page(request: Request, current_user=Depends(get_current_user) if USE_ADVANCED_SECURITY else None):
    return templates.TemplateResponse("user/history.html", {"request": request, "user": current_user})

# Ruta para cerrar sesión
@dashboard_router.get("/logout", name="dashboard_router.logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response
