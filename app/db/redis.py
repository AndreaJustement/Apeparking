import redis
import json
from app.models.sensor import SensorData  

# Redis connection configuration
r = redis.Redis(host='localhost', port=6379, db=0)

def update_sensor_status(sensor_data: SensorData):
    data = sensor_data.dict()
    for sensor, status in data.items():
        r.set(sensor, json.dumps({"status": status}))
