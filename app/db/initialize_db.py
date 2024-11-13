import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Conexión a MongoDB
client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client["ape_parking_db"]

async def initialize_db():
    # Verificar colecciones existentes
    existing_collections = await db.list_collection_names()

    # Crear la colección de usuarios si no existe
    if "users" not in existing_collections:
        usuarios_collection = db["users"]
        await usuarios_collection.create_index("email", unique=True)

    # Crear la colección de espacios de estacionamiento si no existe
    if "parking_spaces" not in existing_collections:
        espacios_collection = db["parking_spaces"]
        await espacios_collection.create_index("space_number", unique=True)

    # Crear la colección de reservas si no existe
    if "reservations" not in existing_collections:
        reservas_collection = db["reservations"]
        await reservas_collection.create_index([("parking_space_id", 1), ("start_time", 1), ("end_time", 1)])

    print("Inicialización de la base de datos completada correctamente.")

if __name__ == "__main__":
    asyncio.run(initialize_db())
