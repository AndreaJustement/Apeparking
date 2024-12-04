from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --------------------------------------
# Crear la aplicación FastAPI
# --------------------------------------
app = FastAPI(debug=True)

# Middleware para manejar CORS
class SimpleCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

# Añadir el middleware
app.add_middleware(SimpleCORSMiddleware)

# --------------------------------------
# Montar archivos estáticos y templates
# --------------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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
# Incluir Routers
# --------------------------------------
app.include_router(auth_router)
app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(reservation_router, tags=["Reservation"])
app.include_router(parking_router, tags=["Parking"])
app.include_router(sensor_router, prefix="/sensors")
app.include_router(payments_router, tags=["Payments"])

# --------------------------------------
# Rutas Generales
# --------------------------------------
@app.get("/", response_class=HTMLResponse)
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
# Rutas de Prueba de Conexión
# --------------------------------------
@app.get("/test-db")
async def test_db():
    """
    Prueba la conexión con la base de datos MongoDB.
    """
    try:
        from app.db.mongodb import get_database
        db = await get_database()
        collections = await db.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/test-redis")
async def test_redis():
    """
    Prueba la conexión con Redis.
    """
    try:
        from app.db.redis import r as redis
        redis.set("test_key", "test_value")
        value = redis.get("test_key")
        return {"status": "success", "value": value.decode("utf-8")}
    except Exception as e:
        return {"status": "error", "details": str(e)}

# --------------------------------------
# Depuración: Mostrar Rutas Activas
# --------------------------------------
@app.on_event("startup")
async def show_routes():
    """
    Mostrar todas las rutas activas al iniciar la aplicación.
    """
    for route in app.routes:
        print(f"Path: {route.path} - Name: {route.name}")
