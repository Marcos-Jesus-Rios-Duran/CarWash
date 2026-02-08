"""
carwash_backend/main.py
principal module to run the carwash backend application

"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from common.config.database import test_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- INICIO ---
    print("Verificando conexión a Base de Datos...")
    status = await test_connection()

    if status == True:
        print("✅ Conexión Exitosa (True)")
    else:
        print("❌Error no se puedo conectar a la base de datos ")

    yield
    # --- APAGADO ---
    print("Apagando aplicación...")

app = FastAPI(lifespan=lifespan)