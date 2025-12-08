"""Verificar roles de usuario"""
from app import create_app
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    
    print("=== USUARIOS EN LA BASE DE DATOS ===\n")
    for user in users:
        print(f"Usuario: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Rol: {user.role}")
        print(f"  Activo: {user.is_active}")
        print()
