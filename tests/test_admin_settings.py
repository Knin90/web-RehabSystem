"""Test para verificar la ruta de configuración"""
from app import create_app, db
from app.models import User, SystemSettings

app = create_app()

with app.test_client() as client:
    with app.app_context():
        # Crear usuario admin si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@test.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        # Login
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        print(f"Login status: {response.status_code}")
        
        # Acceder a settings
        response = client.get('/admin/settings')
        print(f"Settings GET status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de configuración carga correctamente")
            
            # Verificar que settings está en el contexto
            if b'Tema del sistema' in response.data:
                print("✅ Template renderiza correctamente")
            else:
                print("❌ Template no renderiza correctamente")
        else:
            print(f"❌ Error al cargar configuración: {response.status_code}")
        
        # Probar POST
        print("\n=== PROBANDO GUARDADO ===")
        response = client.post('/admin/settings', data={
            'setting_type': 'appearance',
            'theme': 'dark',
            'language': 'en',
            'compact_mode': 'on'
        }, follow_redirects=True)
        
        print(f"Settings POST status: {response.status_code}")
        
        # Verificar que se guardó
        theme = SystemSettings.get_setting('theme')
        language = SystemSettings.get_setting('language')
        
        print(f"\nValores guardados:")
        print(f"  Tema: {theme}")
        print(f"  Idioma: {language}")
        
        if theme == 'dark' and language == 'en':
            print("\n✅ ¡CONFIGURACIONES SE GUARDAN CORRECTAMENTE!")
        else:
            print("\n❌ Las configuraciones NO se guardaron")
