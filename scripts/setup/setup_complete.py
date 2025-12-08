"""
Script todo-en-uno para configurar el sistema completo con pacientes
"""
from app import create_app, db
from app.models import User, Patient, Therapist, Exercise, Routine, RoutineExercise, SystemSettings
from datetime import datetime

app = create_app()

def setup_complete_system():
    """Configurar el sistema completo desde cero"""
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("CONFIGURACIÓN COMPLETA DEL SISTEMA REHABSYSTEM")
        print("=" * 60)
        
        # Paso 1: Limpiar base de datos
        print("\n📋 Paso 1: Limpiando base de datos...")
        db.drop_all()
        db.create_all()
        print("✓ Base de datos limpia")
        
        # Paso 2: Configuraciones del sistema
        print("\n⚙️ Paso 2: Creando configuraciones del sistema...")
        default_settings = {
            'theme': 'light',
            'language': 'es',
            'session_duration': '45',
            'sessions_per_week': '3',
            'rest_time': '30',
            'email_notifications': 'on',
            'appointment_reminder': 'on',
            'progress_report': 'on',
            'detection_accuracy': '85',
            'realtime_analysis': 'on',
            'posture_correction': 'on',
            'capture_fps': '30'
        }
        
        for key, value in default_settings.items():
            SystemSettings.set_setting(key, value)
        print("✓ Configuraciones creadas")
        
        # Paso 3: Crear usuarios base
        print("\n👤 Paso 3: Creando usuarios base...")
        
        # Admin
        admin = User(
            nombre_usuario='admin',
            correo_electronico='admin@rehab.com',
            rol='admin',
            esta_activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("  ✓ Admin creado")
        
        # Terapeuta
        terapeuta_user = User(
            nombre_usuario='terapeuta',
            correo_electronico='tera@rehab.com',
            rol='therapist',
            esta_activo=True
        )
        terapeuta_user.set_password('tera123')
        db.session.add(terapeuta_user)
        db.session.flush()
        
        terapeuta = Therapist(
            id_usuario=terapeuta_user.id,
            nombre_completo='Rafael Lu',
            especialidad='Fisioterapeuta',
            total_pacientes=0
        )
        db.session.add(terapeuta)
        db.session.flush()
        print("  ✓ Terapeuta creado: Rafael Lu")
        
        # Paso 4: Crear ejercicios
        print("\n💪 Paso 4: Creando ejercicios...")
        ejercicios_data = [
            {'nombre': 'Flexiones de rodilla', 'descripcion': 'Ejercicio para fortalecer las rodillas', 'categoria': 'lower', 'repeticiones': '3x15'},
            {'nombre': 'Elevaciones de pierna', 'descripcion': 'Ejercicio para fortalecer piernas', 'categoria': 'lower', 'repeticiones': '3x12'},
            {'nombre': 'Estiramientos lumbares', 'descripcion': 'Ejercicio para estirar la zona lumbar', 'categoria': 'lower', 'repeticiones': '4x30s'},
            {'nombre': 'Rotación de hombros', 'descripcion': 'Ejercicio para movilidad de hombros', 'categoria': 'upper', 'repeticiones': '3x10'},
            {'nombre': 'Flexiones de brazo', 'descripcion': 'Ejercicio para fortalecer brazos', 'categoria': 'upper', 'repeticiones': '3x8'},
            {'nombre': 'Plancha abdominal', 'descripcion': 'Ejercicio para fortalecer core', 'categoria': 'core', 'repeticiones': '3x30s'},
            {'nombre': 'Sentadillas asistidas', 'descripcion': 'Ejercicio para fortalecer piernas', 'categoria': 'lower', 'repeticiones': '3x12'},
            {'nombre': 'Puente de glúteos', 'descripcion': 'Ejercicio para fortalecer glúteos', 'categoria': 'lower', 'repeticiones': '3x15'}
        ]
        
        ejercicios = []
        for ej_data in ejercicios_data:
            ejercicio = Exercise(**ej_data)
            db.session.add(ejercicio)
            ejercicios.append(ejercicio)
        
        db.session.flush()
        print(f"  ✓ {len(ejercicios)} ejercicios creados")
        
        # Paso 5: Crear pacientes
        print("\n🤕 Paso 5: Creando pacientes...")
        pacientes_data = [
            {
                'username': 'paciente',
                'email': 'paci@rehab.com',
                'password': 'paci123',
                'nombre_completo': 'Andrea Luna',
                'diagnostico': 'Rehabilitación rodilla',
                'sesiones_totales': 16,
                'sesiones_completadas': 12
            },
            {
                'username': 'maria_garcia',
                'email': 'maria.garcia@rehab.com',
                'password': 'maria123',
                'nombre_completo': 'María García',
                'diagnostico': 'Lesión de hombro',
                'sesiones_totales': 20,
                'sesiones_completadas': 5
            },
            {
                'username': 'juan_perez',
                'email': 'juan.perez@rehab.com',
                'password': 'juan123',
                'nombre_completo': 'Juan Pérez',
                'diagnostico': 'Rehabilitación de cadera',
                'sesiones_totales': 15,
                'sesiones_completadas': 8
            },
            {
                'username': 'carlos_rodriguez',
                'email': 'carlos.rodriguez@rehab.com',
                'password': 'carlos123',
                'nombre_completo': 'Carlos Rodríguez',
                'diagnostico': 'Lesión lumbar',
                'sesiones_totales': 18,
                'sesiones_completadas': 3
            },
            {
                'username': 'sofia_martinez',
                'email': 'sofia.martinez@rehab.com',
                'password': 'sofia123',
                'nombre_completo': 'Sofía Martínez',
                'diagnostico': 'Rehabilitación de tobillo',
                'sesiones_totales': 12,
                'sesiones_completadas': 10
            }
        ]
        
        pacientes_creados = []
        for pac_data in pacientes_data:
            # Crear usuario
            user = User(
                nombre_usuario=pac_data['username'],
                correo_electronico=pac_data['email'],
                rol='patient',
                esta_activo=True
            )
            user.set_password(pac_data['password'])
            db.session.add(user)
            db.session.flush()
            
            # Crear perfil de paciente
            paciente = Patient(
                id_usuario=user.id,
                nombre_completo=pac_data['nombre_completo'],
                diagnostico=pac_data['diagnostico'],
                progreso=0.0,
                sesiones_totales=pac_data['sesiones_totales'],
                sesiones_completadas=pac_data['sesiones_completadas']
            )
            db.session.add(paciente)
            db.session.flush()
            
            pacientes_creados.append(paciente)
            print(f"  ✓ Paciente creado: {paciente.nombre_completo}")
        
        # Paso 6: Asignar pacientes al terapeuta mediante rutinas
        print("\n📋 Paso 6: Asignando pacientes al terapeuta...")
        for paciente in pacientes_creados:
            # Crear rutina
            rutina = Routine(
                nombre=f'Rutina de {paciente.nombre_completo}',
                descripcion=f'Rutina personalizada para {paciente.diagnostico}',
                id_terapeuta=terapeuta.id,
                id_paciente=paciente.id,
                duracion_minutos=30,
                dificultad='media',
                esta_activa=True
            )
            db.session.add(rutina)
            db.session.flush()
            
            # Agregar 3 ejercicios a la rutina
            for idx, ejercicio in enumerate(ejercicios[:3]):
                ejercicio_rutina = RoutineExercise(
                    id_rutina=rutina.id,
                    id_ejercicio=ejercicio.id,
                    orden=idx,
                    series=3,
                    repeticiones=10,
                    segundos_descanso=30
                )
                db.session.add(ejercicio_rutina)
            
            print(f"  ✓ Rutina asignada a {paciente.nombre_completo}")
        
        # Commit final
        db.session.commit()
        
        # Verificación final
        print("\n" + "=" * 60)
        print("✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
        print("\n📊 RESUMEN:")
        print(f"  - Usuarios: {User.query.count()}")
        print(f"  - Terapeutas: {Therapist.query.count()}")
        print(f"  - Pacientes: {Patient.query.count()}")
        print(f"  - Ejercicios: {Exercise.query.count()}")
        print(f"  - Rutinas: {Routine.query.count()}")
        
        # Verificar asignaciones
        pacientes_asignados = terapeuta.pacientes_asignados
        print(f"\n👥 Pacientes asignados a {terapeuta.nombre_completo}: {len(pacientes_asignados)}")
        for p in pacientes_asignados:
            print(f"  - {p.nombre_completo}")
        
        print("\n📝 CREDENCIALES:")
        print("  Admin: admin / admin123")
        print("  Terapeuta: terapeuta / tera123")
        print("\n  Pacientes:")
        for pac_data in pacientes_data:
            print(f"    - {pac_data['nombre_completo']}: {pac_data['username']} / {pac_data['password']}")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("  1. Reiniciar el servidor Flask:")
        print("     python run.py")
        print("\n  2. Abrir navegador en modo incógnito")
        print("     http://localhost:5000")
        print("\n  3. Login como terapeuta:")
        print("     Usuario: terapeuta")
        print("     Contraseña: tera123")
        print("\n  4. Ir a 'Galería de Videos' y probar compartir")
        print("\n✅ Los 5 pacientes deberían aparecer en el selector")
        
        return True

if __name__ == '__main__':
    try:
        setup_complete_system()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
