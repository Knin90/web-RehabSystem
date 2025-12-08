"""
Script de prueba para verificar las rutas de compartir videos
"""
from app import create_app

def test_routes():
    """Verificar que todas las rutas de compartir videos estén registradas"""
    app = create_app()
    
    print("=" * 60)
    print("VERIFICACIÓN DE RUTAS DE COMPARTIR VIDEOS")
    print("=" * 60)
    
    # Rutas esperadas
    expected_routes = [
        # Terapeuta → Paciente
        ('/api/share-video', ['POST']),
        ('/api/get-patients-for-sharing', ['GET']),
        
        # Paciente → Terapeuta
        ('/api/patient-share-video', ['POST']),
        ('/api/get-patient-therapists', ['GET']),
        
        # Visualización
        ('/api/get-shared-videos', ['GET']),
        ('/api/mark-video-as-read/<int:share_id>', ['POST']),
        ('/api/get-therapist-shared-videos', ['GET']),
        ('/api/therapist-mark-video-as-read/<int:share_id>', ['POST']),
    ]
    
    print("\n📋 Verificando rutas registradas...\n")
    
    found_routes = []
    missing_routes = []
    
    with app.app_context():
        # Obtener todas las rutas registradas
        for rule in app.url_map.iter_rules():
            route_path = str(rule.rule)
            methods = list(rule.methods - {'HEAD', 'OPTIONS'})
            
            # Verificar si es una de las rutas esperadas
            for expected_path, expected_methods in expected_routes:
                if route_path == expected_path:
                    found_routes.append((expected_path, methods))
                    
                    # Verificar métodos
                    if set(expected_methods).issubset(set(methods)):
                        print(f"✓ {expected_path}")
                        print(f"  Métodos: {', '.join(methods)}")
                    else:
                        print(f"⚠ {expected_path}")
                        print(f"  Métodos esperados: {', '.join(expected_methods)}")
                        print(f"  Métodos encontrados: {', '.join(methods)}")
                    print()
    
    # Verificar rutas faltantes
    found_paths = [path for path, _ in found_routes]
    for expected_path, expected_methods in expected_routes:
        if expected_path not in found_paths:
            missing_routes.append(expected_path)
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Rutas esperadas: {len(expected_routes)}")
    print(f"Rutas encontradas: {len(found_routes)}")
    print(f"Rutas faltantes: {len(missing_routes)}")
    
    if missing_routes:
        print("\n❌ Rutas faltantes:")
        for route in missing_routes:
            print(f"  - {route}")
        return False
    else:
        print("\n✅ Todas las rutas están registradas correctamente")
        return True

if __name__ == '__main__':
    import sys
    success = test_routes()
    sys.exit(0 if success else 1)
