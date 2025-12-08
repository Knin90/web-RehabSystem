"""
Test simple para verificar que la API funciona
"""
from app import create_app, db
from app.models import User, Therapist, Patient, Routine

app = create_app()

print("\n" + "=" * 60)
print("TEST SIMPLE DE LA API")
print("=" * 60)

with app.test_client() as client:
    with app.app_context():
        # Verificar que existe el terapeuta
        print("\n1. Verificando terapeuta...")
        terapeuta_user = User.query.filter_by(nombre_usuario='terapeuta').first()
        
        if not terapeuta_user:
            print("❌ Usuario terapeuta no existe")
            print("   Ejecuta: python setup_complete.py")
            exit(1)
        
        print(f"   ✓ Usuario: {terapeuta_user.nombre_usuario}")
        
        terapeuta = Therapist.query.filter_by(id_usuario=terapeuta_user.id).first()
        if not terapeuta:
            print("❌ Perfil de terapeuta no existe")
            exit(1)
        
        print(f"   ✓ Perfil: {terapeuta.nombre_completo}")
        
        # Verificar pacientes asignados
        print("\n2. Verificando pacientes asignados...")
        pacientes = terapeuta.pacientes_asignados
        print(f"   Total: {len(pacientes)}")
        
        if len(pacientes) == 0:
            print("   ❌ No hay pacientes asignados")
            print("   Ejecuta: python setup_complete.py")
            exit(1)
        
        for p in pacientes:
            print(f"   ✓ {p.nombre_completo}")
        
        # Simular login
        print("\n3. Simulando login...")
        with client.session_transaction() as sess:
            sess['_user_id'] = str(terapeuta_user.id)
        
        # Llamar a la API
        print("\n4. Llamando a /api/get-patients-for-sharing...")
        response = client.get('/api/get-patients-for-sharing')
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Success: {data.get('success')}")
            print(f"   Total: {data.get('total')}")
            print(f"   Pacientes: {len(data.get('patients', []))}")
            
            if data.get('success') and data.get('total') > 0:
                print("\n✅ LA API FUNCIONA CORRECTAMENTE")
                print("\n👥 Pacientes que devuelve la API:")
                for p in data.get('patients', []):
                    print(f"   - {p['name']} (ID: {p['id']})")
                
                print("\n🎯 CONCLUSIÓN:")
                print("   La API está funcionando bien.")
                print("   Si no ves los pacientes en el navegador:")
                print("   1. Reinicia el servidor (Ctrl+C → python run.py)")
                print("   2. Abre navegador en modo incógnito")
                print("   3. Login: terapeuta / tera123")
                print("   4. Abre DevTools (F12) → Console")
                print("   5. Intenta compartir un video")
                print("   6. Verifica los logs en la consola")
            else:
                print("\n❌ LA API NO DEVUELVE PACIENTES")
                print("   Ejecuta: python setup_complete.py")
        else:
            print(f"\n❌ ERROR: Status {response.status_code}")
            print("   Verifica que el servidor esté corriendo")

print("\n" + "=" * 60)
