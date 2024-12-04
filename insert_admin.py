import bcrypt
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ape_parking_db"]

# Datos del administrador
admin_data = {
    "email": "admin@example.com",
    "contrasena": bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
    "nombre": "admin",
    "rol": "admin"
}

# Inserción en la colección 'users'
result = db["users"].insert_one(admin_data)
print(f"Administrador insertado con _id: {result.inserted_id}")
