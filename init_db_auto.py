"""
Script para inicializar la base de datos automáticamente en producción
Se ejecuta antes de iniciar gunicorn
"""
from app import create_app, db
from app.models import User, Patient, Therapist, Exercise, SystemSettings, Routine, RoutineExercise
import os

def init_database():
    """Inicializar base de datos si no existe"""
    app = create_app()
    
    with app.app_context():
        try:
            # Intentar crear todas las tablas
            db.create_all()
            print("✓ Tablas creadas/verificadas")
            
            # Verificar si ya hay datos
            user_count = User.query.count()
            
            if user_count == 0:
                print("Base de datos vacía. Creando datos iniciales...")
                
                # Crear admin
                admin = User(
                    nombre_usuario='admin',
                    correo_electronico='admin@rehab.com',
                    rol='admin',
                    esta_activo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                
                # Crear terapeuta
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
                
                # Crear paciente de prueba
                paciente_user = User(
                    nombre_usuario='paciente',
                    correo_electronico='paci@rehab.com',
                    rol='patient',
                    esta_activo=True
                )
                paciente_user.set_password('paci123')
                db.session.add(paciente_user)
                db.session.flush()
                
                paciente = Patient(
                    id_usuario=paciente_user.id,
                    nombre_completo='Andrea Luna',
                    diagnostico='Rehabilitación rodilla',
                    progreso=0.0,
                    sesiones_totales=16,
                    sesiones_completadas=12
                )
                db.session.add(paciente)
                
                # Crear ejercicios básicos
                ejercicios_data = [
                    {'nombre': 'Flexiones de rodilla', 'descripcion': 'Ejercicio para fortalecer las rodillas', 'categoria': 'lower', 'repeticiones': '3x15'},
                    {'nombre': 'Elevaciones de pierna', 'descripcion': 'Ejercicio para fortalecer piernas', 'categoria': 'lower', 'repeticiones': '3x12'},
                    {'nombre': 'Estiramientos lumbares', 'descripcion': 'Ejercicio para estirar la zona lumbar', 'categoria': 'lower', 'repeticiones': '4x30s'},
                ]
                
                for ej_data in ejercicios_data:
                    ejercicio = Exercise(**ej_data)
                    db.session.add(ejercicio)
                
                # Configuraciones básicas
                default_settings = {
                    'theme': 'light',
                    'language': 'es',
                    'session_duration': '45',
                }
                
                for key, value in default_settings.items():
                    SystemSettings.set_setting(key, value)
                
                db.session.commit()
                print("✓ Datos iniciales creados")
                print("  - Admin: admin / admin123")
                print("  - Terapeuta: terapeuta / tera123")
                print("  - Paciente: paciente / paci123")
            else:
                print(f"✓ Base de datos ya tiene datos ({user_count} usuarios)")
                
        except Exception as e:
            print(f"✗ Error al inicializar base de datos: {str(e)}")
            import traceback
            traceback.print_exc()
            # No fallar, continuar con la aplicación
            pass

if __name__ == '__main__':
    init_database()
