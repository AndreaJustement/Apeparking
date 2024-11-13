from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis
import json
from app.db.redis import update_sensor_status  # Función para actualizar estado de sensores en Redis
from app.models.sensor import SensorData  

router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)

@router.websocket("/ws/sensors")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Recibe datos de los sensores
            data = await websocket.receive_text()
            sensor_data = SensorData.parse_raw(data)
            update_sensor_status(sensor_data)
            await websocket.send_text("Datos de sensores recibidos y actualizados")  # Mensaje en español para el usuario
    except WebSocketDisconnect:
        print("Conexión de WebSocket cerrada")

@router.get("/sensors/status")
async def get_sensors_status():
    # Obtiene el estado de cada sensor desde Redis
    status = {}
    for sensor in ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5"]:
        sensor_data = r.get(sensor)
        if sensor_data:
            status[sensor] = json.loads(sensor_data)
    return status
