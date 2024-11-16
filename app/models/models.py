from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from datetime import datetime, timedelta, timezone
from typing import Optional



# Modelo de Espacios de Estacionamiento
class ParkingSpace(BaseModel):
    parking_space_id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    piso: int
    espacio: str
    estado: str = "disponible"  # 'disponible', 'reservado', 'ocupado'
    tipo: str = "estándar"  # 'estándar', 'discapacitados', etc.

    class Config:
        json_encoders = {
            ObjectId: str
        }
        allow_population_by_field_name = True


# Modelo de Pagos
class Payment(BaseModel):
    reservation_id: ObjectId
    amount: float
    payment_method: str
    status: str
    payment_date: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Modelo de Registro de Acciones Administrativas
class AdminActionLog(BaseModel):
    admin_id: ObjectId
    action: str
    description: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Modelos adicionales para actualizaciones y solicitudes
# app/models/reservation.py



class Reservation(BaseModel):
    user_id: ObjectId
    parking_space_id: ObjectId
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    status: str
    reservation_expiration: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=1))

    class Config:
        json_encoders = {
            ObjectId: str
        }

# Modelo de Historial
class HistoryModel(BaseModel):
    user_id: ObjectId
    title: str
    description: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {
            ObjectId: str
        }
