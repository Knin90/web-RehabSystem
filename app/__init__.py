from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates"
    )

    # Configuración
    app.config.from_object('app.config.Config')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'login'

    # Registrar RUTAS PRINCIPALES (admin, patient, therapist TODO dentro de routes.py)
    from app.routes import register_routes
    register_routes(app)

    # ❌ ELIMINADO: admin_routes ya NO existe
    # from app.admin_routes import admin_bp
    # app.register_blueprint(admin_bp, url_prefix="/admin")

    # ❌ ELIMINADO: therapist_routes tampoco se usa porque también está en routes.py
    # from app.therapist_routes import therapist_bp
    # app.register_blueprint(therapist_bp, url_prefix="/therapist")

    return app
