"""
Script para depurar la API de obtener pacientes
"""
from app import create_app, db
from app.models import User, Therapist, Patient
from flask import json

app = create_app()

with app.app_context():
    print("=" * 60)
    print("DEBUG: API GET PATIENTS FOR SHARING")
    print("=" * 60)
    
    # Obtener el usuario terapeuta
    terapeuta_user = User.query.filter_by(nombre_usuario='terapeuta').first()
    if not terapeuta_user:
        print("❌ Usuario terapeuta no encontrado")
        exit(1)
    
    print(f"\n✓ Usuario terapeuta encontrado: {terapeuta_user.nombre_usuario}")
    print(f"  ID: {terapeuta_user.id}")
    print(f"  Rol: {terapeuta_user.rol}")
    
    # Obtener el perfil de terapeuta
    terapeuta = Therapist.query.filter_by(id_usuario=terapeuta_user.id).first()
    if not terapeuta:
        print("❌ Perfil de terapeuta no encontrado")
        exit(1)
    
    print(f"\n✓ Perfil de terapeuta encontrado: {terapeuta.nombre_completo}")
    print(f"  ID: {terapeuta.id}")
    print(f"  Especialidad: {terapeuta.especialidad}")
    
    # Verificar si tiene el atributo pacientes_asignados
    print(f"\n🔍 Verificando atributo 'pacientes_asignados'...")
    if hasattr(terapeuta, 'pacientes_asignados'):
        print("  ✓ Atributo existe")
        
        # Obtener pacientes asignados
        try:
            pacientes = terapeuta.pacientes_asignados
            print(f"  ✓ Pacientes obtenidos: {len(pacientes)}")
            
            if len(pacientes) == 0:
                print("\n⚠️ WARNING: No hay pacientes asignados")
                print("\nVerificando rutinas en la base de datos...")
                
                from app.models import Routine
                rutinas = Routine.query.filter_by(id_terapeuta=terapeuta.id).all()
                print(f"  Rutinas del terapeuta: {len(rutinas)}")
                
                for rutina in rutinas:
                    print(f"    - Rutina ID {rutina.id}: {rutina.nombre}")
                    print(f"      Paciente ID: {rutina.id_paciente}")
                    if rutina.id_paciente:
                        paciente = Patient.query.get(rutina.id_paciente)
                        if paciente:
                            print(f"      Paciente: {paciente.nombre_completo}")
                        else:
                            print(f"      ⚠️ Paciente no encontrado")
            else:
                print("\n📋 LISTA DE PACIENTES ASIGNADOS:")
                print("-" * 60)
                for idx, paciente in enumerate(pacientes, 1):
                    print(f"\n{idx}. {paciente.nombre_completo}")
                    print(f"   ID: {paciente.id}")
                    print(f"   Diagnóstico: {paciente.diagnostico}")
                
                # Simular respuesta de la API
                print("\n" + "=" * 60)
                print("SIMULACIÓN DE RESPUESTA API:")
                print("=" * 60)
                
                patients_list = []
                for patient in pacientes:
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
                
                print(json.dumps(response, indent=2, ensure_ascii=False))
                
        except Exception as e:
            print(f"  ❌ Error al obtener pacientes: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("  ❌ Atributo NO existe")
        print("\n⚠️ El modelo Therapist no tiene el atributo 'pacientes_asignados'")
    
    print("\n" + "=" * 60)
    print("FIN DEL DEBUG")
    print("=" * 60)
