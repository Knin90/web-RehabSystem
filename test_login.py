#!/usr/bin/env python3
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python path:", sys.path[0])
print("Directorio actual:", os.getcwd())

try:
    from app import create_app, db
    from app.models import User
    
    print("Importaciones exitosas")
    
    app = create_app()
    print("App creada")
    
    with app.app_context():
        print("Contexto creado")
        
        # Verificar usuarios
        users = User.query.all()
        print(f"Usuarios encontrados: {len(users)}")
        
        for user in users:
            print(f"  - {user.nombre_usuario} (rol: {user.rol})")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()