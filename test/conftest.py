"""
Configuración global para las pruebas (Fixtures).
Aquí configuramos la base de datos en memoria y el cliente de pruebas.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Importamos tu app y dependencias
from main import app
from common.config.database import Base, get_db
from features.role.models import Role

# Usamos SQLite en memoria (aislado y ultra rápido)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Motor de BD exclusivo para pruebas
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Crea una base de datos fresca para CADA prueba.
    Garantiza que una prueba no afecte a la otra.
    """
    # 1. Crear tablas en memoria
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Iniciar sesión y poblar datos básicos (Roles)
    async with TestingSessionLocal() as session:
        roles_basicos = [
            Role(id=1, name="Admin", description="Admin Role"),
            Role(id=2, name="Cashier", description="Cashier Role"),
            Role(id=3, name="Washer", description="Washer Role"),
            Role(id=4, name="Customer", description="Customer Role")
        ]
        session.add_all(roles_basicos)
        await session.commit()

        yield session # Le entregamos la sesión a la prueba

    # 3. Limpiar todo al terminar la prueba
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """
    Cliente HTTP de prueba (El 'Postman' automatizado).
    Sobrescribe la dependencia de tu base de datos real.
    """
    # Función para interceptar tu get_db original
    async def override_get_db():
        yield db_session

    # Le decimos a FastAPI que use la BD de prueba en lugar de la real
    app.dependency_overrides[get_db] = override_get_db

    # Configuramos el cliente asíncrono para pegarle a tus endpoints
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Limpiamos los overrides al terminar
    app.dependency_overrides.clear()