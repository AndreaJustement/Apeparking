from datetime import datetime
from pymongo.database import Database
from bson import ObjectId

async def process_payment(reservation_id: str, db: Database):
    reservation = await db["reservations"].find_one({"_id": ObjectId(reservation_id)})
    if not reservation:
        raise Exception("Reservation not found")

    # Calcular el tiempo de ocupación
    end_time = datetime.utcnow()
    start_time = reservation["start_time"]
    duration = (end_time - start_time).total_seconds() / 3600  # En horas
    cost = round(duration * 2, 2)  # $2 por hora

    # Actualizar estado de la reserva
    await db["reservations"].update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": {"status": "finalizada", "end_time": end_time, "cost": cost}},
    )

    # Liberar la plaza
    await db["parking_spaces"].update_one(
        {"_id": reservation["parking_space_id"]}, {"$set": {"estado": "disponible"}}
    )

    # Registrar el pago
    payment = {
        "reservation_id": ObjectId(reservation_id),
        "user_id": reservation["user_id"],
        "amount": cost,
        "payment_date": datetime.utcnow(),
        "payment_method": "credit_card",
        "transaction_id": "TXN123456789",
        "status": "completed",
    }
    await db["payments"].insert_one(payment)

    return {"message": "Payment processed successfully", "cost": cost}
