"""
Script para inicializar Flask-Migrate
"""
from app import create_app, db
from flask_migrate import init, migrate, upgrade
import os

app = create_app()

with app.app_context():
    # Verificar si ya existe el directorio migrations
    if not os.path.exists('migrations'):
        print("Inicializando Flask-Migrate...")
        os.system('flask db init')
        print("✓ Flask-Migrate inicializado")
    else:
        print("✓ Flask-Migrate ya está inicializado")
    
    print("\nCreando migración inicial...")
    os.system('flask db migrate -m "Initial migration"')
    print("✓ Migración creada")
    
    print("\nAplicando migración...")
    os.system('flask db upgrade')
    print("✓ Migración aplicada")
    
    print("\n✅ Base de datos lista!")
