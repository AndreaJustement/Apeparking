from pymongo import MongoClient

try:
    # Usa el nombre correcto de la base de datos
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ape_parking_db"]  # Aquí está el nombre exacto de la base de datos
    print("Conexión exitosa")
    print("Colecciones disponibles:", db.list_collection_names())
except Exception as e:
    print("Error de conexión:", e)
