"""
Script rápido para verificar si los pacientes están asignados al terapeuta
"""
from app import create_app, db
from app.models import User, Therapist, Patient, Routine

app = create_app()

with app.app_context():
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DE PACIENTES ASIGNADOS")
    print("=" * 70)
    
    # Verificar terapeuta
    print("\n1️⃣ Verificando terapeuta...")
    terapeuta_user = User.query.filter_by(nombre_usuario='terapeuta').first()
    
    if not terapeuta_user:
        print("❌ ERROR: Usuario 'terapeuta' no existe")
        print("\n🔧 SOLUCIÓN: Ejecuta 'python setup_complete.py'")
        exit(1)
    
    print(f"✅ Usuario encontrado: {terapeuta_user.nombre_usuario}")
    
    terapeuta = Therapist.query.filter_by(id_usuario=terapeuta_user.id).first()
    if not terapeuta:
        print("❌ ERROR: Perfil de terapeuta no existe")
        print("\n🔧 SOLUCIÓN: Ejecuta 'python setup_complete.py'")
        exit(1)
    
    print(f"✅ Perfil encontrado: {terapeuta.nombre_completo}")
    
    # Verificar pacientes
    print("\n2️⃣ Verificando pacientes en la base de datos...")
    total_pacientes = Patient.query.count()
    print(f"   Total de pacientes en BD: {total_pacientes}")
    
    if total_pacientes == 0:
        print("❌ ERROR: No hay pacientes en la base de datos")
        print("\n🔧 SOLUCIÓN: Ejecuta 'python setup_complete.py'")
        exit(1)
    
    # Verificar rutinas
    print("\n3️⃣ Verificando rutinas del terapeuta...")
    rutinas = Routine.query.filter_by(id_terapeuta=terapeuta.id).all()
    print(f"   Total de rutinas creadas: {len(rutinas)}")
    
    rutinas_con_paciente = [r for r in rutinas if r.id_paciente is not None]
    print(f"   Rutinas asignadas a pacientes: {len(rutinas_con_paciente)}")
    
    if len(rutinas_con_paciente) == 0:
        print("❌ ERROR: No hay rutinas asignadas a pacientes")
        print("\n🔧 SOLUCIÓN: Ejecuta 'python setup_complete.py'")
        exit(1)
    
    # Verificar pacientes asignados
    print("\n4️⃣ Verificando pacientes asignados al terapeuta...")
    pacientes_asignados = terapeuta.pacientes_asignados
    print(f"   Pacientes asignados: {len(pacientes_asignados)}")
    
    if len(pacientes_asignados) == 0:
        print("❌ ERROR: El terapeuta no tiene pacientes asignados")
        print("\n🔧 SOLUCIÓN: Ejecuta 'python setup_complete.py'")
        exit(1)
    
    print("\n👥 LISTA DE PACIENTES ASIGNADOS:")
    print("-" * 70)
    for idx, paciente in enumerate(pacientes_asignados, 1):
        print(f"   {idx}. {paciente.nombre_completo}")
        print(f"      - ID: {paciente.id}")
        print(f"      - Diagnóstico: {paciente.diagnostico}")
        print(f"      - Usuario: {paciente.usuario.nombre_usuario}")
        print()
    
    # Simular respuesta de la API
    print("5️⃣ Simulando respuesta de la API...")
    print("-" * 70)
    
    patients_list = []
    for patient in pacientes_asignados:
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
    
    import json
    print(json.dumps(response, indent=2, ensure_ascii=False))
    print("-" * 70)
    
    # Resultado final
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN EXITOSA")
    print("=" * 70)
    
    print(f"\n📊 RESUMEN:")
    print(f"   - Terapeuta: {terapeuta.nombre_completo}")
    print(f"   - Pacientes asignados: {len(pacientes_asignados)}")
    print(f"   - Rutinas creadas: {len(rutinas_con_paciente)}")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("   1. Asegúrate de que el servidor Flask esté corriendo:")
    print("      python run.py")
    print()
    print("   2. Abre el navegador en modo incógnito")
    print()
    print("   3. Login como terapeuta:")
    print("      Usuario: terapeuta")
    print("      Contraseña: tera123")
    print()
    print("   4. Ve a 'Galería de Videos'")
    print()
    print("   5. Intenta compartir un video")
    print()
    print("   6. Abre la consola del navegador (F12)")
    print()
    print(f"   7. Deberías ver {len(pacientes_asignados)} pacientes en el selector:")
    for p in pacientes_asignados:
        print(f"      - {p.nombre_completo}")
    
    print("\n💡 SI NO VES LOS PACIENTES:")
    print("   - Abre DevTools (F12) → Console")
    print("   - Busca los mensajes que empiezan con '🔍 DEBUG:'")
    print("   - Verifica que diga 'Número de pacientes: 5'")
    print("   - Si dice '0', el problema es de autenticación")
    print("   - Si dice '5' pero no aparecen, es problema de JavaScript/DOM")
    
    print("\n" + "=" * 70)
