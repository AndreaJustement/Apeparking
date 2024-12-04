from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

from pydantic import BaseModel
from typing import Optional

class ParkingSpace(BaseModel):
    _id: str
    floor: int
    space_number: str
    status: str  # "libre", "reservado", "ocupado"
    sensor_id: Optional[str]  # Asociado al sensor
