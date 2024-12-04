from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings


# Crear el cliente MongoDB asíncrono con timeout
client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

# Acceso a la base de datos
db = client[settings.DATABASE_NAME]


# Función para obtener la base de datos (usada con Depends en FastAPI)
def get_database():
    return db


# Prueba de conexión asíncrona
async def test_mongodb_connection():
    try:
        # Verifica si MongoDB está disponible
        await client.server_info()
        print("Conexión a MongoDB exitosa")
    except ServerSelectionTimeoutError as e:
        print(f"Error de conexión a MongoDB: {e}")
        raise e  # Lanza el error para manejo en FastAPI o logs
