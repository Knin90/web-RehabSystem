"""
Script para probar la obtención de pacientes asignados al terapeuta
"""
from app import create_app, db
from app.models import Therapist, Patient

app = create_app()

with app.app_context():
    # Obtener el terapeuta
    terapeuta = Therapist.query.first()
    
    if not terapeuta:
        print("❌ No se encontró ningún terapeuta")
        exit(1)
    
    print("=" * 60)
    print(f"TERAPEUTA: {terapeuta.nombre_completo}")
    print("=" * 60)
    
    # Obtener pacientes asignados usando la propiedad
    print("\n📋 Obteniendo pacientes asignados...")
    pacientes_asignados = terapeuta.pacientes_asignados
    
    print(f"\n✓ Total de pacientes asignados: {len(pacientes_asignados)}")
    print("\n" + "-" * 60)
    
    if len(pacientes_asignados) == 0:
        print("⚠ No hay pacientes asignados al terapeuta")
        print("\nPara asignar pacientes, ejecuta:")
        print("  python seed_more_patients.py")
    else:
        print("LISTA DE PACIENTES:")
        print("-" * 60)
        for idx, paciente in enumerate(pacientes_asignados, 1):
            print(f"\n{idx}. {paciente.nombre_completo}")
            print(f"   ID: {paciente.id}")
            print(f"   Diagnóstico: {paciente.diagnostico}")
            print(f"   Sesiones: {paciente.sesiones_completadas}/{paciente.sesiones_totales}")
            print(f"   Usuario: {paciente.usuario.nombre_usuario}")
    
    print("\n" + "=" * 60)
    
    # Simular la respuesta de la API
    print("\n📡 SIMULACIÓN DE RESPUESTA API:")
    print("-" * 60)
    
    patients_list = []
    for patient in pacientes_asignados:
        patients_list.append({
            'id': patient.id,
            'name': patient.nombre_completo,
            'diagnosis': patient.diagnostico or 'Sin diagnóstico'
        })
    
    import json
    print(json.dumps({
        'success': True,
        'patients': patients_list,
        'total': len(patients_list)
    }, indent=2, ensure_ascii=False))
    
    print("\n✅ Prueba completada exitosamente")
