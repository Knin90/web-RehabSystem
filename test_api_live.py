"""
Script para probar la API en vivo como lo haría el navegador
"""
from app import create_app
from flask import json
import sys

app = create_app()

def test_api_with_login():
    """Probar la API con autenticación simulada"""
    
    with app.test_client() as client:
        print("=" * 60)
        print("PRUEBA DE API EN VIVO - GET PATIENTS FOR SHARING")
        print("=" * 60)
        
        # Paso 1: Login como terapeuta
        print("\n📝 Paso 1: Login como terapeuta...")
        login_response = client.post('/login', data={
            'nombre_usuario': 'terapeuta',
            'contrasena': 'tera123'
        }, follow_redirects=True)
        
        if login_response.status_code in [200, 302]:
            print("✓ Login exitoso")
        else:
            print(f"❌ Login falló: {login_response.status_code}")
            return False
        
        # Paso 2: Llamar a la API
        print("\n📡 Paso 2: Llamando a /api/get-patients-for-sharing...")
        api_response = client.get('/api/get-patients-for-sharing')
        
        print(f"Status Code: {api_response.status_code}")
        
        if api_response.status_code == 200:
            print("✓ API respondió correctamente")
            
            # Parsear respuesta JSON
            try:
                data = json.loads(api_response.data)
                print("\n📋 RESPUESTA DE LA API:")
                print("-" * 60)
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("-" * 60)
                
                if data.get('success'):
                    patients = data.get('patients', [])
                    total = data.get('total', 0)
                    
                    print(f"\n✅ Success: {data['success']}")
                    print(f"✅ Total de pacientes: {total}")
                    
                    if total == 0:
                        print("\n⚠️ WARNING: No hay pacientes en la respuesta")
                        print("\n🔧 SOLUCIÓN:")
                        print("   1. Ejecuta: python setup_complete.py")
                        print("   2. Reinicia el servidor")
                        print("   3. Prueba nuevamente")
                        return False
                    else:
                        print("\n👥 LISTA DE PACIENTES:")
                        for idx, patient in enumerate(patients, 1):
                            print(f"   {idx}. {patient.get('name')} - {patient.get('diagnosis')}")
                        
                        print("\n✅ La API está funcionando correctamente")
                        print("✅ Los pacientes están siendo devueltos")
                        
                        # Verificar estructura de datos
                        print("\n🔍 Verificando estructura de datos...")
                        if patients:
                            first_patient = patients[0]
                            required_fields = ['id', 'name', 'diagnosis']
                            missing_fields = [f for f in required_fields if f not in first_patient]
                            
                            if missing_fields:
                                print(f"⚠️ Campos faltantes: {missing_fields}")
                            else:
                                print("✓ Estructura de datos correcta")
                        
                        return True
                else:
                    print(f"\n❌ API devolvió success=false")
                    print(f"   Mensaje: {data.get('message', 'Sin mensaje')}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error al parsear JSON: {e}")
                print(f"   Respuesta raw: {api_response.data}")
                return False
        else:
            print(f"❌ API respondió con error: {api_response.status_code}")
            print(f"   Respuesta: {api_response.data}")
            return False

if __name__ == '__main__':
    try:
        success = test_api_with_login()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ PRUEBA EXITOSA")
            print("=" * 60)
            print("\n🎯 CONCLUSIÓN:")
            print("   La API está funcionando correctamente.")
            print("   Si aún no ves los pacientes en el navegador:")
            print("\n   1. Abre DevTools (F12)")
            print("   2. Ve a la pestaña 'Network'")
            print("   3. Intenta compartir un video")
            print("   4. Busca la petición 'get-patients-for-sharing'")
            print("   5. Verifica la respuesta")
            print("\n   Si la respuesta es diferente a esta prueba,")
            print("   puede haber un problema de caché o sesión.")
        else:
            print("❌ PRUEBA FALLIDA")
            print("=" * 60)
            print("\n🔧 ACCIONES RECOMENDADAS:")
            print("   1. python setup_complete.py")
            print("   2. python run.py")
            print("   3. Abrir navegador en modo incógnito")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
