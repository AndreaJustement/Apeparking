import os
import redis
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Conexión a MongoDB (asincrónica)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/ape_parking_db")
client = AsyncIOMotorClient(MONGO_URI)
db = client["ape_parking_db"]

# Conexión a Redis (sincronizada)
REDIS_URI = os.getenv("REDIS_URI", "redis://redis:6379")
redis_client = redis.StrictRedis.from_url(REDIS_URI)

# Inicialización de colecciones (MongoDB)
async def initialize_db():
    # Verificar colecciones existentes
    existing_collections = await db.list_collection_names()

    if "user" not in existing_collections:
        usuarios_collection = db["user"]
        await usuarios_collection.create_index("email", unique=True)

    if "parking_spaces" not in existing_collections:
        espacios_collection = db["parking_spaces"]
        await espacios_collection.create_index("space_number", unique=True)

    if "reservations" not in existing_collections:
        reservas_collection = db["reservations"]
        await reservas_collection.create_index(
            [("parking_space_id", 1), ("start_time", 1), ("end_time", 1)]
        )

    print("Inicialización de la base de datos completada correctamente.")

# Función para verificar las conexiones
async def check_connections():
    try:
        # Prueba MongoDB
        await db.command("ping")
        print("Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

    try:
        # Prueba Redis
        redis_client.ping()
        print("Conexión a Redis exitosa.")
    except Exception as e:
        print(f"Error al conectar a Redis: {e}")
