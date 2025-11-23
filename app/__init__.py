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
    app = Flask(__name__, 
                template_folder='../rehab-system/templates',
                static_folder='../rehab-system/static')
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'login'
    
    from app.routes import register_routes
    register_routes(app)
    
    return app