import os
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.routes import router
from src.contact.infraestructure.ConsumerLambda.ConsumerContac import ContactConsumer

# Cargar las variables del archivo .env
dotenv_path = "/path/to/.env"
load_dotenv(dotenv_path, encoding="utf-8")

app = FastAPI()

# Inicializar el limitador
limiter = Limiter(key_func=get_remote_address)

# Configuración de CORS
origins = ["http://localhost", "https://localhost"]
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
    consumer = ContactConsumer()
    await asyncio.to_thread(consumer.start_consuming)

# Iniciar el consumidor de contactos cuando arranque FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_contact_consumer())

if __name__ == "__main__":
    # Leer las variables de entorno
    port = int(os.getenv("PORT", 4000))
    use_ssl = os.getenv("USE_SSL", "False") == "True"
    ssl_certfile = os.getenv("SSL_CERTFILE")
    ssl_keyfile = os.getenv("SSL_KEYFILE")

    if use_ssl and ssl_certfile and ssl_keyfile:
        # Ejecutar con SSL
        uvicorn.run("main:app", host="0.0.0.0", port=port, ssl_certfile=ssl_certfile, ssl_keyfile=ssl_keyfile)
    else:
        # Si no tienes SSL configurado, forzar redirección
        # Puedes usar un proxy como nginx o manejar la redirección en FastAPI

        @app.middleware("http")
        async def redirect_http_to_https(request, call_next):
            if request.url.scheme == "http":
                url = request.url.replace(scheme="https")
                return RedirectResponse(url)
            response = await call_next(request)
            return response

        uvicorn.run("main:app", host="0.0.0.0", port=port)
