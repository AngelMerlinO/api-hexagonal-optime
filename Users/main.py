import os
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.routes import router
from src.contact.infraestructure.ConsumerLambda.ConsumerContac import ContactConsumer  # Ajusta la importación según tu estructura de proyecto

# Cargar las variables del archivo .env
load_dotenv()

app = FastAPI()

# Inicializar el limitador
limiter = Limiter(key_func=get_remote_address)

# Configuración de CORS (si es necesario)
origins = ["http://localhost", "https://localhost"]  # Ajusta según necesites
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar el limitador como middleware
app.state.limiter = limiter

# Registrar las rutas
app.include_router(router)

# Configurar el ContactConsumer en segundo plano
async def start_contact_consumer():
    # Instanciar el consumidor
    consumer = ContactConsumer()
    
    # Iniciar el consumidor en un hilo asincrónico
    await asyncio.to_thread(consumer.start_consuming)

# Iniciar el consumidor de contactos cuando arranque FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_contact_consumer())

if __name__ == "__main__":
    # Leer las variables de entorno
    port = int(os.getenv("PORT", 8000))
    use_ssl = os.getenv("USE_SSL", "False") == "True"
    ssl_certfile = os.getenv("SSL_CERTFILE")
    ssl_keyfile = os.getenv("SSL_KEYFILE")

    # Ejecutar con SSL si está habilitado en el entorno
    if use_ssl and ssl_certfile and ssl_keyfile:
        uvicorn.run("main:app", host="0.0.0.0", port=port, ssl_certfile=ssl_certfile, ssl_keyfile=ssl_keyfile)
    else:
        # Ejecutar sin SSL si no está configurado
        uvicorn.run("main:app", host="0.0.0.0", port=port)