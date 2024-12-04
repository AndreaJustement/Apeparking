from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.reservations_service import ReservationService
from app.db.mongodb import get_database
from app.db.redis import r
from bson import ObjectId
import json
from datetime import datetime, timezone, timedelta
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Ruta para mostrar la página de reservas
@router.get("/reservations/", response_class=HTMLResponse)
async def view_reservations_page(request: Request, db=Depends(get_database)):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        user_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    service = ReservationService(db, r)

    # Obtener espacios y reservas
    spaces = await db["parking_spaces"].find({}).to_list(100)
    reservations = await service.get_user_reservations(user_id)

    return templates.TemplateResponse(
        "reservation.html",
        {
            "request": request,
            "available_spaces": [s for s in spaces if s["estado"] == "disponible"],
            "reservations": reservations,
        },
    )

# Ruta para crear una reserva
@router.post("/reservations/")
async def create_reservation(user_id: str, db=Depends(get_database)):
    service = ReservationService(db, r)
    try:
        result = await service.create_reservation(user_id)
        return JSONResponse(content=result)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Ruta para cancelar una reserva
@router.delete("/reservations/{reservation_id}")
async def cancel_reservation(reservation_id: str, db=Depends(get_database)):
    service = ReservationService(db, r)
    try:
        result = await service.cancel_reservation(reservation_id)
        return JSONResponse(content=result)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
