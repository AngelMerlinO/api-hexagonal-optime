import os
import sys  # Para modificar el sys.path
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.database import DATABASE_URL

# Añadir el directorio 'src' al sys.path para que Python pueda encontrar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Cargar las variables del archivo .env
load_dotenv()

# Configurar la URL de la base de datos
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpretar la configuración del archivo alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importar el modelo de SQLAlchemy
from users.domain.User import Base  # Asegúrate de que 'Base' se importe correctamente

# Añadir los metadatos de tus modelos (user.domain.User) para generar migraciones
target_metadata = Base.metadata

# Funciones de run_migrations que Alembic utiliza para aplicar migraciones
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