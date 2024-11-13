from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings


# Crear el cliente MongoDB asíncrono
client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

# Acceso a la base de datos
db = client["ape_parking_db"]

# Función para obtener la base de datos
def get_database():
    return db

# Colección de usuarios
usuarios_collection = db["usuarios"]
parking_collection = db["parking_spaces"]

# Prueba de conexión
try:
    client.server_info()  # Verifica si el servidor está disponible
except ServerSelectionTimeoutError as e:
    print(f"Error de conexión a MongoDB: {e}")

