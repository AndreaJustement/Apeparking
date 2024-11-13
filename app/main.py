from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

# --------------------------------------
# Importaciones y Configuración del Sistema
# --------------------------------------
import sys
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# --------------------------------------
# Importar Routers
# --------------------------------------
from app.routers.auth_router import auth_router
from app.routers.dashboard_router import dashboard_router
from app.routers.admin_router import admin_router
from app.routers.parking_routes import router as parking_router
from app.routers.sensors.sensor_router import router as sensor_router
from app.routers.reservation_router import router as reservation_router
from app.routers.payments_router import router as payments_router


# --------------------------------------
# Crear la aplicación FastAPI
# --------------------------------------
app = FastAPI(debug=True)

# --------------------------------------
# Montar Archivos Estáticos y Templates
# --------------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --------------------------------------
# Importar Dependencias y Servicios de BD
# --------------------------------------
from app.db.redis import r as redis
from app.db.initialize_db import initialize_db

# --------------------------------------
# Incluir Routers con Prefijos y Etiquetas
# --------------------------------------

app.include_router(auth_router, tags=["Auth"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(reservation_router, tags=["Reservation"])
app.include_router(parking_router, tags=["Parking"])
app.include_router(sensor_router, prefix="/sensors", tags=["Sensors"])
app.include_router(payments_router, tags=["Payments"])

# --------------------------------------
# Rutas Generales
# --------------------------------------
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ayuda", response_class=HTMLResponse)
async def mostrar_ayuda(request: Request):
    return templates.TemplateResponse("ayuda.html", {"request": request})

@app.get("/logout", name="logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization")
    return response

# --------------------------------------
# Depuración: Imprimir Rutas Activas
# --------------------------------------
for route in app.routes:
    print(f"Path: {route.path} - Name: {route.name}")
