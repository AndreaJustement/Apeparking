from datetime import datetime, timedelta
from bson import ObjectId
from app.db.mongodb import db
from pymongo.errors import PyMongoError
from app.security.dependencies import get_current_user, is_admin
from motor.motor_asyncio import AsyncIOMotorDatabase

async def reservar_espacio(user_id: str, parking_space_id: str, start_time: datetime, end_time: datetime):
    try:
        # Convertir IDs a ObjectId
        user_id = ObjectId(user_id)
        parking_space_id = ObjectId(parking_space_id)

        # Lógica para reservar un espacio de estacionamiento
        reserva_expiracion = datetime.utcnow() + timedelta(minutes=15)  # Cambiado a UTC
        nueva_reserva = {
            "user_id": user_id,
            "parking_space_id": parking_space_id,
            "start_time": start_time,
            "end_time": end_time,
            "status": "activa",
            "reservation_expiration": reserva_expiracion
        }

        # Verificar que el espacio esté disponible antes de reservar
        espacio = await db.parking_spaces.find_one({"_id": parking_space_id})
        if espacio and espacio["estado"] == "disponible":
            # Insertar nueva reserva y actualizar el espacio
            await db.reservations.insert_one(nueva_reserva)
            await db.parking_spaces.update_one({"_id": parking_space_id}, {"$set": {"estado": "reservado"}})
            return {"msg": "Reserva creada con éxito"}
        else:
            return {"error": "El espacio no está disponible para reservar"}
    except PyMongoError as e:
        # Manejar cualquier error relacionado con MongoDB
        return {"error": f"Error al crear la reserva: {str(e)}"}

async def liberar_espacio_si_reserva_expira():
    try:
        # Lógica para liberar un espacio si la reserva expira
        reservas_expiradas = await db.reservations.find({
            "status": "activa",
            "reservation_expiration": {"$lt": datetime.utcnow()}  # Cambiado a UTC
        }).to_list(100)

        for reserva in reservas_expiradas:
            # Actualizar el estado del espacio y de la reserva
            await db.parking_spaces.update_one({"_id": reserva['parking_space_id']}, {"$set": {"estado": "disponible"}})
            await db.reservations.update_one({"_id": reserva['_id']}, {"$set": {"status": "cancelada"}})
    except PyMongoError as e:
        # Manejar cualquier error relacionado con MongoDB
        print(f"Error al liberar las reservas expiradas: {e}")
