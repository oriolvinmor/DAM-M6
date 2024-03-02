from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .config import DATABASE_URI
from sqlalchemy import create_engine
from .base import Base

engine = create_engine(DATABASE_URI)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas definidas en Base en la base de datos
Base.metadata.create_all(bind=engine)

# Configuración de la conexión a la base de datos
def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos.")
    except OperationalError as e:
        print("Error al conectar con la base de datos:", e)

