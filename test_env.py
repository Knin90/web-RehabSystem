import os
from dotenv import load_dotenv

# Cargar variables
load_dotenv()

# Verificar
variables = {
    'FLASK_ENV': os.getenv('FLASK_ENV'),
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'DATABASE_URL': os.getenv('DATABASE_URL'),
}

print("=== VARIABLES DE ENTORNO ===")
for key, value in variables.items():
    status = "✅" if value else "❌"
    # Ocultar valor completo de SECRET_KEY
    if key == 'SECRET_KEY' and value:
        value = value[:10] + "..." if len(value) > 10 else value
    print(f"{status} {key}: {value}")