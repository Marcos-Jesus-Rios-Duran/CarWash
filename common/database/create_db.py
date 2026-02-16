"""
carwash_backend/common/database/create_db.py
Script to manage the database schema lifecycle (Create, Drop, and Update).
"""

import asyncio
import sys
from pathlib import Path

# Setup the root path to allow absolute imports from common and features
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# pylint: disable=wrong-import-position, unused-import
from common.config.database import engine, Base
from features.role.models import Role
from features.user.models import User
from features.service.models import Service
from features.vehicle.models import Vehicle
from features.appointment.models import Appointment
# pylint: enable=wrong-import-position, unused-import


class DatabaseManager:
    """
    Handles database schema operations following SRP.
    Exclusively manages table creation, destruction, and selective updates.
    """

    def __init__(self, db_engine, metadata):
        """Initialize with database engine and metadata."""
        self.engine = db_engine
        self.metadata = metadata

    async def create_all_tables(self):
        """Creates all tables defined in the models if they do not exist."""
        print("🚀 Iniciando la creación de tablas...")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)
        print("✅ Tablas creadas exitosamente.")

    async def drop_all_tables(self):
        """Drops all tables from the database. Use with extreme caution."""
        print("⚠️  Eliminando todas las tablas existentes...")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.drop_all)
        print("🗑️  Base de datos limpiada por completo.")

    async def update_table(self, table_name: str):
        """
        Drops and recreates a single table by its name.
        Useful for applying model changes without a full reset.
        """
        print(f"🔄 Actualizando la tabla: {table_name}...")
        async with self.engine.begin() as conn:
            table = self.metadata.tables.get(table_name)
            if table is not None:
                # Perform drop and create within the sync context
                await conn.run_sync(table.drop)
                await conn.run_sync(table.create)
                print(f"✅ Tabla '{table_name}' actualizada con éxito.")
            else:
                print(f"❌ Error: La tabla '{table_name}' no existe en los modelos.")

    async def reset_database(self):
        """Wipes the database and recreates the entire schema from scratch."""
        await self.drop_all_tables()
        await self.create_all_tables()


async def main():
    """Main entry point for database management CLI."""
    # List models to ensure they are loaded into Base.metadata for Pylint
    _ = [Role, User, Service, Vehicle, Appointment]

    manager = DatabaseManager(engine, Base.metadata)

    # CLI Logic
    if "--reset" in sys.argv:
        await manager.reset_database()
    elif "--update" in sys.argv:
        try:
            # Usage: python create_db.py --update <table_name>
            target_table = sys.argv[sys.argv.index("--update") + 1]
            await manager.update_table(target_table)
        except (IndexError, ValueError):
            print("❌ Error: Especifica la tabla. Ej: --update users")
    else:
        await manager.create_all_tables()

    await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Operación cancelada por el usuario.")
