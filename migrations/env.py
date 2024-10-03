# migrations/env.py

import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Añadir el directorio 'src' al sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

# Configurar la URL de la base de datos
config = context.config

# Importar la URL de la base de datos y Base
from config.database import DATABASE_URL, Base
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpretar la configuración del archivo alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importar los modelos para que Alembic los detecte
from src.users.domain.User import User
from src.schedules.domain.Schedule import Schedule
from src.schedules.domain.ScheduleItem import ScheduleItem
from src.notifications.domain.Notification import Notification
from src.Activities.domain.Activities import Activities


# Establecer los metadatos de los modelos
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()