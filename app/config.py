import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret Key para sesiones y CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///rehab.db')
    
    # Fix para PostgreSQL en Render (postgres:// → postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Agregar parámetros SSL a la URL si es PostgreSQL
    if SQLALCHEMY_DATABASE_URI and 'postgresql://' in SQLALCHEMY_DATABASE_URI:
        if '?' not in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '?sslmode=require'
        elif 'sslmode' not in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '&sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Engine options para PostgreSQL en Render
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verificar conexiones antes de usar
        'pool_recycle': 300,    # Reciclar conexiones cada 5 minutos
        'pool_size': 10,
        'max_overflow': 20,
    }
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    ALLOWED_EXTENSIONS = {'webm', 'mp4', 'jpg', 'jpeg', 'png'}
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
