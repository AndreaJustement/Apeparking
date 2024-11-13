from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from app.db.mongodb import get_database
from app.db.redis import r
import json

router = APIRouter()

@router.post("/reservations/")
async def create_reservation(user_id: str, space_number: str, db=Depends(get_database)):
    # Obtener el sensor_id del espacio desde MongoDB
    space = await db["parking_spaces"].find_one({"space_number": space_number})
    if not space:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")

    sensor_key = space["sensor_id"]
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

#Cancelar una Reserva
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
    space = await db["parking_spaces"].find_one({"space_number": space_number})
    sensor_key = space["sensor_id"]
    r.set(sensor_key, json.dumps({"estado": 0}))

    return JSONResponse(content={"message": "Reserva cancelada"})
