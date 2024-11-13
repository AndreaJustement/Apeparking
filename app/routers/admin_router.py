from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.auth_service import is_admin
from app.core.config import USE_ADVANCED_SECURITY
from pymongo.database import Database
from bson import ObjectId
from app.db.mongodb import get_database

admin_router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")

# Ruta del dashboard del administrador
@admin_router.get("/dashboard", response_class=HTMLResponse, name="admin_dashboard")
async def admin_dashboard(request: Request, admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# Ver todos los espacios de estacionamiento
@admin_router.get("/view_parking_spaces", response_class=HTMLResponse)
async def view_parking_spaces(request: Request, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    parking_spaces = await db["parking_spaces"].find().to_list(100)
    for space in parking_spaces:
        space["_id"] = str(space["_id"])  # Convierte ObjectId a string para evitar errores
    return templates.TemplateResponse("admin_parking_spaces.html", {"request": request, "parking_spaces": parking_spaces})


# Crear un nuevo espacio de estacionamiento
@admin_router.get("/add_parking_space", response_class=HTMLResponse)
async def add_parking_space_form(request: Request, admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    return templates.TemplateResponse("add_parking_space.html", {"request": request})

@admin_router.post("/admin/add_parking_space")
async def add_parking_space(request: Request, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    form_data = await request.form()
    new_space = {
        "id": form_data.get("id"),
        "floor": form_data.get("Piso"),
        "space_number": form_data.get("Espacio"),
        "available": form_data.get("Estado") == "Disponible"  # Conversión a booleano
    }
    await db["parking_spaces"].insert_one(new_space)
    return RedirectResponse(url="/admin/view_parking_spaces", status_code=303)


# Actualizar espacio de estacionamiento
@admin_router.get("/edit_parking_space/{space_id}", response_class=HTMLResponse)
async def edit_parking_space(space_id: str, request: Request, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    space = await db["parking_spaces"].find_one({"_id": ObjectId(space_id)})
    return templates.TemplateResponse("edit_parking_space.html", {"request": request, "space": space})

@admin_router.post("/edit_parking_space/{space_id}")
async def update_parking_space(space_id: str, request: Request, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    form_data = await request.form()
    updated_space = {
        "piso": int(form_data["piso"]),
        "espacio": form_data["espacio"],
        "estado": form_data["estado"],
        "tipo": form_data["tipo"]
    }
    await db["parking_spaces"].update_one({"_id": ObjectId(space_id)}, {"$set": updated_space})
    return RedirectResponse(url="/admin/view_parking_spaces", status_code=303)

# Eliminar espacio de estacionamiento
@admin_router.get("/delete_parking_space/{space_id}")
async def delete_parking_space(space_id: str, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    await db["parking_spaces"].delete_one({"_id": ObjectId(space_id)})
    return RedirectResponse(url="/admin/view_parking_spaces", status_code=303)

# Ver todos los usuarios
@admin_router.get("/manage_users", response_class=HTMLResponse)
async def manage_users(request: Request, db: Database = Depends(get_database)):
    usuarios = await db["users"].find().to_list(100)
    return templates.TemplateResponse("manage_users.html", {"request": request, "usuarios": usuarios})


# Eliminar usuario

@admin_router.post("/delete_user/{user_id}")
async def delete_user(user_id: str, db: Database = Depends(get_database), admin=Depends(is_admin) if USE_ADVANCED_SECURITY else None):
    # Verificar si el usuario existe antes de eliminarlo
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Proceder a eliminar el usuario si existe
    await db["users"].delete_one({"_id": ObjectId(user_id)})
    return RedirectResponse(url="/admin/manage_users", status_code=303)

