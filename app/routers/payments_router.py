from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from pymongo.database import Database  # Asegúrate de usar el tipo correcto para `Database`
from app.templates import templates  # Confirma que `templates` esté configurado correctamente
from app.services.payments_service import process_payment  # Importa la lógica del servicio de pagos
from app.db.mongodb import get_database  # Usa la función correcta para obtener la base de datos

router = APIRouter()

@router.get("/user/payments", response_class=HTMLResponse, name="view_payments_page")
async def view_payments_page(request: Request, db: Database = Depends(get_database)):
    """
    Muestra la página de pagos con las reservas pendientes y el historial de pagos.
    """
    # Recupera las reservas activas y el historial de pagos
    pending_reservations = await db["reservations"].find({"status": "activa"}).to_list(length=100)
    payment_history = await db["payments"].find().to_list(length=100)

    # Renderiza la plantilla payments.html con los datos
    return templates.TemplateResponse(
        "user/payments.html",  # Asegúrate de que el archivo esté en templates/user/payments.html
        {"request": request, "pending_reservations": pending_reservations, "payment_history": payment_history},
    )

@router.post("/payments/process", name="process_payment_endpoint")
async def process_payment_endpoint(reservation_id: str, db: Database = Depends(get_database)):
    """
    Procesa un pago asociado a una reserva.
    """
    # Procesa el pago usando el servicio de pagos
    result = await process_payment(reservation_id, db)
    return result
