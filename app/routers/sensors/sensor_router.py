from fastapi import APIRouter, HTTPException, Request, Depends
import redis
import json

# Conexión a Redis
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

# Define el router
router = APIRouter()

@router.get("/get_sensor/{space_number}", tags=["Sensors"])
async def get_sensor_status(space_number: int):
    try:
        sensor_key = f"sensor_{space_number}"
        sensor_data = redis_client.get(sensor_key)
        if not sensor_data:
            raise HTTPException(
                status_code=404,
                detail=f"Sensor {sensor_key} no encontrado."
            )
        return {"space_number": space_number, "data": json.loads(sensor_data)}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el sensor: {str(e)}"
        )

@router.post("/update", tags=["Sensors"])
async def update_sensor_status(request: Request):
    try:
        # Obtener datos y registrarlos para depuración
        data = await request.json()
        print(f"Datos recibidos: {data}")  # Log para revisar el contenido
        
        # Extraer valores y forzar a enteros (evitar errores por tipos)
        try:
            space_number = int(data.get("space_number", -1))  # Valor por defecto: -1
            status = int(data.get("status", -1))  # Valor por defecto: -1
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="space_number y status deben ser enteros."
            )

        # Validaciones de rango
        if space_number < 0 or status not in [0, 1]:
            raise HTTPException(
                status_code=400,
                detail="space_number debe ser >= 0 y status debe ser 0 o 1."
            )

        # Clave y guardado en Redis
        sensor_key = f"sensor_{space_number}"
        redis_client.set(sensor_key, json.dumps({"estado": status}))
        print(f"Actualización exitosa: {sensor_key} -> {status}")

        return {
            "status": "success",
            "message": f"Sensor {sensor_key} actualizado correctamente.",
            "space_number": space_number,
            "status": status
        }
    except HTTPException as http_ex:
        print(f"Error HTTP: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor."
        )
