"""
Script para simular exactamente lo que hace el navegador
"""
from app import create_app, db
from app.models import User, Therapist
from flask import json

app = create_app()

print("=" * 60)
print("SIMULACIÓN DE NAVEGADOR - COMPARTIR VIDEO")
print("=" * 60)

with app.app_context():
    # Simular que el usuario ya está logueado
    print("\n🔍 Verificando usuario terapeuta...")
    
    terapeuta_user = User.query.filter_by(nombre_usuario='terapeuta').first()
    if not terapeuta_user:
        print("❌ Usuario terapeuta no encontrado")
        print("\n🔧 Ejecuta: python setup_complete.py")
        exit(1)
    
    print(f"✓ Usuario encontrado: {terapeuta_user.nombre_usuario}")
    print(f"  ID: {terapeuta_user.id}")
    print(f"  Rol: {terapeuta_user.rol}")
    
    terapeuta = Therapist.query.filter_by(id_usuario=terapeuta_user.id).first()
    if not terapeuta:
        print("❌ Perfil de terapeuta no encontrado")
        exit(1)
    
    print(f"✓ Perfil encontrado: {terapeuta.nombre_completo}")
    
    # Simular la llamada a la API
    print("\n📡 Simulando llamada a /api/get-patients-for-sharing...")
    print("-" * 60)
    
    try:
        # Obtener pacientes asignados (esto es lo que hace la ruta)
        assigned_patients = terapeuta.pacientes_asignados if hasattr(terapeuta, 'pacientes_asignados') else []
        
        patients_list = []
        for patient in assigned_patients:
            patients_list.append({
                'id': patient.id,
                'name': patient.nombre_completo,
                'diagnosis': patient.diagnostico or 'Sin diagnóstico'
            })
        
        response = {
            'success': True,
            'patients': patients_list,
            'total': len(patients_list)
        }
        
        print("RESPUESTA JSON:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("-" * 60)
        
        if response['total'] == 0:
            print("\n⚠️ WARNING: No hay pacientes asignados")
            print("\n🔧 SOLUCIÓN:")
            print("   python setup_complete.py")
            exit(1)
        
        print(f"\n✅ Total de pacientes: {response['total']}")
        print("\n👥 PACIENTES QUE DEBERÍAN APARECER EN EL SELECTOR:")
        for idx, patient in enumerate(patients_list, 1):
            print(f"   {idx}. {patient['name']} - {patient['diagnosis']}")
        
        # Simular el HTML que se genera en el navegador
        print("\n📝 HTML QUE SE DEBERÍA GENERAR:")
        print("-" * 60)
        print('<select id="sharePatientSelect">')
        print('  <option value="">Selecciona un paciente...</option>')
        for patient in patients_list:
            print(f'  <option value="{patient["id"]}">{patient["name"]} - {patient["diagnosis"]}</option>')
        print('</select>')
        print("-" * 60)
        
        print("\n" + "=" * 60)
        print("✅ SIMULACIÓN COMPLETADA")
        print("=" * 60)
        
        print("\n🎯 CONCLUSIÓN:")
        print(f"   La API debería devolver {response['total']} pacientes.")
        print("   Si no los ves en el navegador, el problema puede ser:")
        print("\n   1. ❌ No estás logueado como terapeuta")
        print("      Solución: Login con terapeuta / tera123")
        print("\n   2. ❌ Caché del navegador")
        print("      Solución: Ctrl + Shift + R o modo incógnito")
        print("\n   3. ❌ Servidor no reiniciado")
        print("      Solución: Ctrl + C → python run.py")
        print("\n   4. ❌ Error de JavaScript")
        print("      Solución: F12 → Console → Ver errores")
        
        print("\n📋 PASOS PARA VERIFICAR EN EL NAVEGADOR:")
        print("   1. Abrir DevTools (F12)")
        print("   2. Ir a pestaña 'Network'")
        print("   3. Intentar compartir un video")
        print("   4. Buscar petición 'get-patients-for-sharing'")
        print("   5. Ver la respuesta (debería ser igual a la de arriba)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
