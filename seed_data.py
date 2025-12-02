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
    
    # Crear usuarios
    admin = User(username='admin', email='admin@rehab.com', role='admin')
    admin.set_password('admin123')
    
    terapeuta_user = User(username='terapeuta', email='tera@rehab.com', role='therapist')
    terapeuta_user.set_password('tera123')
    
    paciente_user = User(username='paciente', email='paci@rehab.com', role='patient')
    paciente_user.set_password('paci123')
    
    db.session.add_all([admin, terapeuta_user, paciente_user])
    db.session.commit()
    
    # Crear perfiles
    terapeuta = Therapist(user_id=terapeuta_user.id, full_name='Rafael Lu', specialty='Fisioterapeuta')
    paciente = Patient(user_id=paciente_user.id, full_name='Andrea Luna', 
                      diagnosis='Rehabilitación rodilla', total_sessions=16, completed_sessions=12)
    
    db.session.add_all([terapeuta, paciente])
    db.session.commit()
    
    # Crear ejercicios
    ejercicios = [
        Exercise(name='Flexiones de rodilla', repetitions='3x15', category='inferior'),
        Exercise(name='Elevaciones de pierna', repetitions='3x12', category='inferior'),
        Exercise(name='Estiramientos', repetitions='4x30seg', category='estiramiento')
    ]
    db.session.add_all(ejercicios)
    db.session.commit()
    
    print("✅ Base de datos inicializada!")
    print("\n📝 Credenciales:")
    print("Admin: admin / admin123")
    print("Terapeuta: terapeuta / tera123")
    print("Paciente: paciente / paci123")