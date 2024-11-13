import json
from app.db.redis import r as redis_client

def update_parking_spot(spot_id, status):
    """
    Actualiza el estado de un espacio de parking en Redis.
    :param spot_id: ID del espacio de parking (ej. "sensor1")
    :param status: Estado del espacio (0 para libre, 1 para ocupado)
    """
    redis_client.set(spot_id, json.dumps({"estado": status}))

def get_parking_status():
    """
    Obtiene el estado de todos los espacios de parking desde Redis.
    :return: Diccionario con el estado de cada espacio.
    """
    keys = redis_client.keys("sensor*")
    status = {key.decode("utf-8"): json.loads(redis_client.get(key).decode("utf-8")) for key in keys}
    return status
