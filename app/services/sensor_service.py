import redis
import socket
import json
from pymongo import MongoClient
from datetime import datetime

# Configuración de Redis y MongoDB
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
mongo_client = MongoClient("mongodb://mongo:27017")
db = mongo_client["ape_parking_db"]

# Configuración del ESP32
ESP32_IP = "192.168.102.83"  # Cambia por la IP del ESP32
ESP32_PORT = 8080

# Función para conectar al ESP32 y leer datos en tiempo real
def connect_to_sensors():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ESP32_IP, ESP32_PORT))
            print("Conectado al ESP32")
            while True:
                data = s.recv(1024).decode("utf-8")
                if not data:
                    break

                # Convertir los datos recibidos en JSON
                sensor_data = json.loads(data)
                print(f"Datos recibidos: {sensor_data}")

                # Actualizar el estado en Redis y MongoDB
                update_sensor_status(sensor_data)
    except Exception as e:
        print(f"Error al conectar con el ESP32: {e}")

# Función para actualizar Redis y MongoDB
def update_sensor_status(sensor_data):
    try:
        for sensor_id, status in sensor_data.items():
            # Actualizar Redis
            redis_client.set(sensor_id, status)

            # Actualizar MongoDB
            db.parking_spaces.update_one(
                {"sensor_id": sensor_id},
                {"$set": {"estado": "ocupado" if status == "1" else "disponible"}}
            )
            print(f"Sensor {sensor_id} actualizado a {status}")
    except Exception as e:
        print(f"Error al actualizar el estado del sensor: {e}")

# Función para obtener el estado de un sensor desde Redis
def get_sensor_status(sensor_id):
    return redis_client.get(sensor_id)

# Función para obtener todos los estados de los sensores
def get_all_sensors_status():
    keys = redis_client.keys()
    return {key: redis_client.get(key) for key in keys}
