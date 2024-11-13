from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class ParkingSpace(BaseModel):
    id: Optional[ObjectId]       # ID único de MongoDB
    floor: int                   # Piso donde se encuentra el espacio
    space_number: str            # Identificador alfanumérico del espacio (ej. "A1", "A2")
    sensor_id: str               # ID del sensor (ej. "sensor1")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
