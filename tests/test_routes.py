"""Script para probar las rutas del admin"""
from app import create_app

app = create_app()

with app.app_context():
    # Listar todas las rutas
    print("=== RUTAS REGISTRADAS ===\n")
    
    admin_routes = []
    for rule in app.url_map.iter_rules():
        if 'admin' in rule.rule:
            admin_routes.append((rule.rule, rule.endpoint, list(rule.methods)))
    
    # Ordenar y mostrar
    for route, endpoint, methods in sorted(admin_routes):
        methods_str = ', '.join(m for m in methods if m not in ['HEAD', 'OPTIONS'])
        print(f"{route:40} -> {endpoint:30} [{methods_str}]")
    
    print(f"\n✅ Total de rutas admin: {len(admin_routes)}")
    
    # Verificar rutas específicas
    print("\n=== VERIFICACIÓN DE RUTAS NUEVAS ===\n")
    
    required_routes = [
        '/admin/settings',
        '/admin/export-data',
        '/admin/export/<data_type>'
    ]
    
    all_routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    for route in required_routes:
        if route in all_routes:
            print(f"✅ {route}")
        else:
            print(f"❌ {route} - NO ENCONTRADA")
