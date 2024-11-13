from fastapi import APIRouter, Depends
from app.db.mongodb import get_database
from app.db.redis import r
import json

router = APIRouter()

@router.get("/parking/status")
async def get_parking_status(admin: bool = False, db=Depends(get_database)):
    parking_status = []

    # Obtener todos los espacios de estacionamiento desde MongoDB
    parking_spaces = await db["parking_spaces"].find({"floor": 1}).to_list(100)

    for space in parking_spaces:
        sensor_key = space["sensor_id"]  # Usar sensor_id para la clave en Redis
        sensor_data = r.get(sensor_key)
        
        # Determinar disponibilidad en base al valor en Redis
        available = True if not sensor_data else json.loads(sensor_data).get("estado") == 0
        
        # Añadir la información para el usuario y, opcionalmente, el sensor_id para el administrador
        space_info = {
            "floor": space["floor"],
            "space_number": space["space_number"],
            "available": available
        }
        if admin:
            space_info["sensor_id"] = space["sensor_id"]

        parking_status.append(space_info)

    return {"parking_status": parking_status}
