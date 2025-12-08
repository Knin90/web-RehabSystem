from app import create_app, db
from app.models import User, Patient, Therapist, Exercise, SystemSettings

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Crear configuraciones por defecto
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
    
    # Crear usuarios (usar los nombres de columnas definidos en models.py)
    admin = User(
        nombre_usuario='admin',
        correo_electronico='admin@rehab.com',
        rol='admin'
    )
    admin.set_password('admin123')
    
    terapeuta_user = User(
        nombre_usuario='terapeuta',
        correo_electronico='tera@rehab.com',
        rol='therapist'
    )
    terapeuta_user.set_password('tera123')
    
    paciente_user = User(
        nombre_usuario='paciente',
        correo_electronico='paci@rehab.com',
        rol='patient'
    )
    paciente_user.set_password('paci123')
    
    db.session.add_all([admin, terapeuta_user, paciente_user])
    db.session.commit()
    
    # Crear perfiles (usar nombres de campos reales)
    terapeuta = Therapist(
        id_usuario=terapeuta_user.id,
        nombre_completo='Rafael Lu',
        especialidad='Fisioterapeuta'
    )
    paciente = Patient(
        id_usuario=paciente_user.id,
        nombre_completo='Andrea Luna',
        diagnostico='Rehabilitación rodilla',
        sesiones_totales=16,
        sesiones_completadas=12
    )
    
    db.session.add_all([terapeuta, paciente])
    db.session.commit()
    
    # Crear ejercicios (usar nombres de columnas en español)
    ejercicios = [
        Exercise(nombre='Flexiones de rodilla', repeticiones='3x15', categoria='inferior'),
        Exercise(nombre='Elevaciones de pierna', repeticiones='3x12', categoria='inferior'),
        Exercise(nombre='Estiramientos', repeticiones='4x30seg', categoria='estiramiento')
    ]
    db.session.add_all(ejercicios)
    db.session.commit()
    
    print("✅ Base de datos inicializada!")
    print("\n📝 Credenciales:")
    print("Admin: admin / admin123")
    print("Terapeuta: terapeuta / tera123")
    print("Paciente: paciente / paci123")
