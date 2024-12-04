
# **ApeParking - Sistema de Localización de Estacionamientos**

Este proyecto es un sistema de localización de plazas de estacionamiento, diseñado para integrar funcionalidades IoT con sensores, manejo de reservas y pagos. El backend está desarrollado con **FastAPI**, utilizando **MongoDB** para el almacenamiento y **Redis** para actualizaciones en tiempo real.

---

## **Requisitos previos**

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

1. **Git** - Para clonar el repositorio.
   - Descargar e instalar: [https://git-scm.com/](https://git-scm.com/)
2. **Docker y Docker Compose** - Para ejecutar los contenedores.
   - Descargar e instalar Docker: [https://www.docker.com/](https://www.docker.com/)

---

## **Cómo clonar el repositorio**

1. Abre tu terminal o línea de comandos.
2. Navega al directorio donde deseas clonar el proyecto.
3. Ejecuta el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/AndreaJustement/Apeparking.git
   ```

4. Ingresa al directorio del proyecto clonado:

   ```bash
   cd Apeparking
   ```

---

## **Configuración inicial**

1. Crea un archivo `.env` en la raíz del proyecto. Este archivo contiene las variables de entorno necesarias para la configuración. Puedes usar el siguiente ejemplo:

   ```env
   MONGO_URI=mongodb://apeparking-mongo:27017/apeparkingbd
   REDIS_HOST=apeparking-redis
   REDIS_PORT=6379
   SECRET_KEY=your-secret-key
   ```

2. **Asegúrate de que los puertos necesarios estén libres:**
   - Puerto 8000 (para la aplicación)
   - Puerto 6379 (para Redis)
   - Puerto 27017 (para MongoDB)

---

## **Ejecutar el proyecto con Docker**

1. En la raíz del proyecto, ejecuta el siguiente comando para iniciar los contenedores:

   ```bash
   docker-compose up -d
   ```

   Esto levantará:
   - **FastAPI** en el puerto `8000`.
   - **Redis** en el puerto `6379`.
   - **MongoDB** en el puerto `27017`.

2. Verifica que los contenedores están corriendo:

   ```bash
   docker ps
   ```

3. Abre tu navegador y accede a la aplicación en:

   ```
   http://localhost:8000
   ```

---

## **Estructura del proyecto**

- **app/**: Contiene el código fuente de la aplicación.
  - **routers/**: Rutas del backend (reservas, usuarios, pagos, etc.).
  - **models/**: Modelos para la base de datos (MongoDB).
  - **services/**: Lógica de negocio y servicios.
  - **static/**: Archivos estáticos (CSS, imágenes).
  - **templates/**: Plantillas HTML.
  - **db/**: Configuración de MongoDB y Redis.
  - **core/**: Configuración de variables de entorno y settings.

- **docker-compose.yml**: Archivo para configurar los servicios Docker.
- **Dockerfile**: Configuración para el contenedor de la aplicación.

---

## **Comandos útiles**

### Detener los contenedores
```bash
docker-compose down
```

### Ver los logs de los contenedores
```bash
docker-compose logs -f
```

### Reconstruir los contenedores después de cambios en el código
```bash
docker-compose up -d --build
```





