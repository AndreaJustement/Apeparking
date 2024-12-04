import redis
import json
from app.models.sensor import SensorData

# Configuración de conexión a Redis
r = redis.StrictRedis(host="redis", port=6379, db=0)

# Actualizar el estado de los sensores
async def update_sensor_status(sensor_data: SensorData):
    data = sensor_data.dict()
    for sensor, status in data.items():
        r.set(sensor, json.dumps({"status": status}))

# Obtener estado de un sensor
def get_sensor_status(sensor_id: str):
    data = r.get(sensor_id)
    return json.loads(data) if data else None
