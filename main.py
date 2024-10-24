import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.routes import router

# Cargar las variables del archivo .env
load_dotenv()

app = FastAPI()

# Configuración de CORS (si es necesario)
origins = ["http://localhost", "https://localhost"]  # Ajusta según necesites
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(router)

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
