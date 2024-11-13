from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()  # Asegúrate de que el nombre del enrutador es `router`

templates = Jinja2Templates(directory="app/templates")  

@router.get("/payments")  # Cambia `payments_router` por `router`
async def payments(request: Request):
    return templates.TemplateResponse("payments.html", {"request": request})

# Agregar cualquier otra ruta relacionada con pagos aquí
