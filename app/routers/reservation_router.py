from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone, timedelta

from app.core.config import USE_ADVANCED_SECURITY


from bson import ObjectId
from app.db.mongodb import get_database
from app.db.redis import r
import json
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/reservations/", response_class=HTMLResponse)
async def view_reservations_page(request: Request, db=Depends(get_database), user=Depends(get_current_user) if USE_ADVANCED_SECURITY else None):
    # Verificar que el usuario exista en la base de datos
    if USE_ADVANCED_SECURITY and not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = user["_id"] if USE_ADVANCED_SECURITY else request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Asegúrate de que el `user_id` sea un ObjectId válido si es necesario
    try:
        user_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Obtener espacios disponibles y reservas activas del usuario
    available_spaces = await db["parking_spaces"].find({"available": True}).to_list(100)
    user_reservations = await db["reservations"].find({"user_id": user_id, "status": "activo"}).to_list(100)

    return templates.TemplateResponse("reservation.html", {
        "request": request,
        "available_spaces": available_spaces,
        "user_reservations": user_reservations,
        "user_id": user_id
    })


# Ruta para crear una reserva
@router.post("/reservations/")
async def create_reservation(user_id: str, space_number: str, db=Depends(get_database)):
    # Verificar que el usuario exista en la base de datos
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar disponibilidad en Redis usando el sensor
    sensor_key = f"sensor{space_number}"
    sensor_data = r.get(sensor_key)
    if sensor_data and json.loads(sensor_data).get("estado") == 1:
        raise HTTPException(status_code=400, detail="El espacio de estacionamiento no está disponible")

    # Crear la reserva en MongoDB
    reservation = {
        "user_id": ObjectId(user_id),
        "space_number": space_number,
        "start_time": datetime.now(timezone.utc),
        "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
        "status": "activo"
    }
    result = await db["reservations"].insert_one(reservation)
    
    # Marcar el espacio como ocupado en Redis
    r.set(sensor_key, json.dumps({"estado": 1}))

    return JSONResponse(content={"message": "Reserva creada", "reservation_id": str(result.inserted_id)})

# Ruta para cancelar una reserva
@router.delete("/reservations/{reservation_id}")
async def cancel_reservation(reservation_id: str, db=Depends(get_database)):
    # Verificar si la reserva existe
    reservation = await db["reservations"].find_one({"_id": ObjectId(reservation_id)})
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # Eliminar la reserva
    await db["reservations"].delete_one({"_id": ObjectId(reservation_id)})

    # Marcar el espacio como libre en Redis
    space_number = reservation["space_number"]
    sensor_key = f"sensor{space_number}"
    r.set(sensor_key, json.dumps({"estado": 0}))

    return JSONResponse(content={"message": "Reserva cancelada"})
