from fastapi import FastAPI
from src.routes import router

app = FastAPI()

# Registrar todas las rutas de la aplicación
app.include_router(router)