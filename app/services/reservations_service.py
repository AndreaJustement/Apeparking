from datetime import datetime, timezone, timedelta
from bson import ObjectId
from fastapi import HTTPException, Depends
from app.db.mongodb import get_database
from app.db.redis import r
import json


class ReservationService:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    # Mapeo de sensores a espacios
    sensor_to_space_map = {
        "sensor1": {"space": "A1", "floor": 1},
        "sensor2": {"space": "A2", "floor": 1},
        "sensor3": {"space": "B1", "floor": 2},
        "sensor4": {"space": "B2", "floor": 2},
        "sensor5": {"space": "B3", "floor": 2},
    }

    # Asignar espacio disponible desde sensores
    async def assign_space_from_sensor(self):
        for sensor, details in self.sensor_to_space_map.items():
            sensor_data = self.redis_client.get(sensor)
            if sensor_data and json.loads(sensor_data).get("estado") == 0:  # Libre
                # Verifica en la BD si el espacio no está reservado
                space = await self.db["parking_spaces"].find_one(
                    {"espacio": details["space"], "estado": "disponible"}
                )
                if space:
                    return details
        raise HTTPException(
            status_code=400, detail="No hay espacios disponibles en este momento"
        )

    # Crear reserva
    async def create_reservation(self, user_id: str):
        try:
            user_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        # Verificar existencia del usuario
        user = await self.db["users"].find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Asignar espacio disponible
        assigned_space = await self.assign_space_from_sensor()

        # Crear reserva
        reservation = {
            "user_id": user_id,
            "space_number": assigned_space["space"],
            "floor": assigned_space["floor"],
            "start_time": datetime.now(timezone.utc),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "status": "activo",
        }
        result = await self.db["reservations"].insert_one(reservation)

        # Actualizar estado del sensor y espacio
        self.redis_client.set(
            f"sensor{assigned_space['space']}", json.dumps({"estado": 1})
        )
        await self.db["parking_spaces"].update_one(
            {"espacio": assigned_space["space"]}, {"$set": {"estado": "ocupado"}}
        )

        return {
            "message": f"Reserva creada en espacio {assigned_space['space']} (Piso {assigned_space['floor']})",
            "reservation_id": str(result.inserted_id),
        }

    # Cancelar reserva
    async def cancel_reservation(self, reservation_id: str):
        try:
            reservation_id = ObjectId(reservation_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid reservation ID format")

        # Verificar que la reserva existe
        reservation = await self.db["reservations"].find_one({"_id": reservation_id})
        if not reservation:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")

        # Eliminar reserva
        await self.db["reservations"].delete_one({"_id": reservation_id})

        # Liberar espacio en Redis y BD
        space_number = reservation["space_number"]
        sensor_key = f"sensor{space_number}"
        self.redis_client.set(sensor_key, json.dumps({"estado": 0}))
        await self.db["parking_spaces"].update_one(
            {"espacio": space_number}, {"$set": {"estado": "disponible"}}
        )

        return {"message": "Reserva cancelada"}
