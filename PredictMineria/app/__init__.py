from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar las rutas
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app