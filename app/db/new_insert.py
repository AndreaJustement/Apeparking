from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta, timezone  # Añadir timezone aquí

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ape_parking_db"]  # Nombre de la base de datos

# Verificar bases de datos y colecciones
print("Bases de datos disponibles:", client.list_database_names())
print("Colecciones en ape_parking_db:", db.list_collection_names())

# Función para crear una reserva dinámica
def create_dynamic_reservation(user_email, parking_space_number):
    # Buscar el usuario por email
    user = db["users"].find_one({"email": user_email})
    if not user:
        print("Usuario no encontrado.")
        return
   
    # Buscar el espacio de estacionamiento por número o ID
    parking_space = db["parking_spaces"].find_one({"space_number": parking_space_number, "available": True})
    print("Espacio de estacionamiento encontrado:", parking_space)  # Agrega esta línea
    if not parking_space:
        print("Espacio de estacionamiento no disponible o no encontrado.")
        return

    # Crear la reserva
    reservation = {
        "user_id": user["_id"],
        "parking_space_id": parking_space["_id"],
        "start_time": datetime.now(timezone.utc),  # Usar timezone.utc aquí
        "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
        "status": "active",
        "reservation_expiration": datetime.now(timezone.utc) + timedelta(days=1)
    }
    
    # Insertar la reserva en la colección `reservations`
    db["reservations"].insert_one(reservation)
    
    # Cambiar el estado del espacio a 'reservado'
    db["parking_spaces"].update_one({"_id": parking_space["_id"]}, {"$set": {"estado": "reservado"}})

    print("Reserva creada exitosamente.")

# Ejemplo de uso
create_dynamic_reservation("user2@example.com", "B")  
