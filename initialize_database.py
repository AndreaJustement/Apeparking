from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta, timezone

# Configuración de conexión a MongoDB
client = MongoClient("mongodb://mongo:27017")  # Usar el host 'mongo' por Docker
db = client["ape_parking_db"]

# Verificar bases de datos y colecciones existentes
print("Bases de datos disponibles:", client.list_database_names())
print("Colecciones actuales:", db.list_collection_names())

# Crear datos iniciales
def initialize_data():
    # Usuarios iniciales
    users = [
        {"_id": ObjectId(), "email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"_id": ObjectId(), "email": "user1@example.com", "password": "user123", "role": "user"},
        {"_id": ObjectId(), "email": "user2@example.com", "password": "user123", "role": "user"}
    ]
    db["users"].insert_many(users)

    # Espacios de estacionamiento iniciales
    parking_spaces = [
        {"_id": ObjectId(), "space_number": "A", "floor": 1, "estado": "libre"},
        {"_id": ObjectId(), "space_number": "B", "floor": 1, "estado": "libre"},
        {"_id": ObjectId(), "space_number": "C", "floor": 2, "estado": "ocupado"}
    ]
    db["parking_spaces"].insert_many(parking_spaces)

    # Reserva inicial
    reservations = [
        {
            "_id": ObjectId(),
            "user_id": users[1]["_id"],
            "parking_space_id": parking_spaces[0]["_id"],
            "start_time": datetime.now(timezone.utc),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=2),
            "status": "active"
        }
    ]
    db["reservations"].insert_many(reservations)

    print("Datos iniciales creados exitosamente.")

# Ejecutar inicialización
initialize_data()
