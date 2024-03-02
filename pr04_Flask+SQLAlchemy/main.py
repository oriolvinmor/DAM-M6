from flask import Flask
from src.api.routes import init_api_routes
from config.db import Base, engine, test_connection

app = Flask(__name__)

# Inicializar las rutas de la API
init_api_routes(app)

test_connection()

if __name__ == '__main__':
    # Crear todas las tablas definidas en Base en la base de datos
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
