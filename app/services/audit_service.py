from datetime import datetime
from bson import ObjectId
from app.security.dependencies import get_current_user, is_admin
from app.db.mongodb import get_database
from typing import Optional

class AdminAuditLog:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db["audit_logs"]

    async def log_action(
        self,
        admin_id: ObjectId,
        action: str,
        object_type: str,
        object_id: str,
        description: Optional[str] = None,
        admin_ip: Optional[str] = None
    ):
        """
        Registra una acción administrativa en el log de auditoría.
        """
        log_entry = {
            "admin_id": admin_id,
            "action": action,  # Ej. 'create', 'delete', 'update'
            "object_type": object_type,  # Ej. 'parking_space'
            "object_id": object_id,
            "timestamp": datetime.utcnow(),
            "description": description,
            "admin_ip": admin_ip
        }
        await self.collection.insert_one(log_entry)

# Uso de la clase
async def log_admin_action(
    db: Database,
    admin_id: ObjectId,
    action: str,
    object_type: str,
    object_id: str,
    description: Optional[str] = None,
    admin_ip: Optional[str] = None
):
    """
    Función que facilita el registro de acciones de auditoría de administración.
    """
    audit_log = AdminAuditLog(db)
    await audit_log.log_action(
        admin_id=admin_id,
        action=action,
        object_type=object_type,
        object_id=object_id,
        description=description,
        admin_ip=admin_ip
    )
