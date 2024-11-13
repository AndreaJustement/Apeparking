from datetime import datetime
from app.db.mongodb import db
from app.security.dependencies import get_current_user, is_admin

async def procesar_pago(reservation_id, amount, payment_method):
    reserva = await db.reservations.find_one({"_id": reservation_id, "status": "activa"})
    if not reserva:
        raise Exception("Reserva no encontrada o ya completada")

    nuevo_pago = {
        "reservation_id": reservation_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "completado",
        "payment_date": datetime.now()
    }
    await db.payments.insert_one(nuevo_pago)
    await db.reservations.update_one({"_id": reservation_id}, {"$set": {"status": "completada"}})
