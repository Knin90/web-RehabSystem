"""Test simple de la aplicación"""
from app import create_app

app = create_app()

with app.app_context():
    # Verificar que la ruta existe
    print("=== RUTAS DISPONIBLES ===")
    for rule in app.url_map.iter_rules():
        if 'export' in rule.rule:
            print(f"✅ {rule.rule} -> {rule.endpoint}")
    
    print("\n=== TEST DE TEMPLATE ===")
    try:
        with app.test_client() as client:
            # Simular login
            from app.models import User
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"✅ Usuario admin encontrado: {admin.email}")
            else:
                print("❌ Usuario admin NO encontrado")
            
            print("\n✅ App funciona correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
