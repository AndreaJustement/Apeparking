from pydantic import BaseModel

class SensorData(BaseModel):
    sensor1: int  # 0 para libre, 1 para ocupado
    sensor2: int
    sensor3: int
    sensor4: int
    sensor5: int
