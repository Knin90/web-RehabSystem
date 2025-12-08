#!/usr/bin/env python
"""Script para inicializar la base de datos en producción"""

from app import create_app, db
from app.models import User, Patient, Therapist
from werkzeug.security import generate_password_hash

def init_database():
    app = create_app()
    
    with app.app_context():
        print("🔄 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas")
        
        # Verificar si ya existen usuarios
        if User.query.first():
            print("⚠️ La base de datos ya tiene usuarios")
            return
        
        print("🔄 Creando usuarios de prueba...")
        
        # Admin
        admin = User(
            username='admin',
            email='admin@rehab.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Terapeuta
        therapist_user = User(
            username='terapeuta',
            email='terapeuta@rehab.com',
            role='therapist',
            is_active=True
        )
        therapist_user.set_password('tera123')
        db.session.add(therapist_user)
        
        # Paciente
        patient_user = User(
            username='paciente',
            email='paciente@rehab.com',
            role='patient',
            is_active=True
        )
        patient_user.set_password('paci123')
        db.session.add(patient_user)
        
        db.session.commit()
        print("✅ Usuarios creados")
        
        # Crear perfil de terapeuta
        therapist = Therapist(
            user_id=therapist_user.id,
            full_name='Dr. Juan Pérez',
            specialty='Fisioterapia',
            total_patients=0
        )
        db.session.add(therapist)
        
        # Crear perfil de paciente
        patient = Patient(
            user_id=patient_user.id,
            full_name='María García',
            diagnosis='Rehabilitación de rodilla',
            progress=0,
            completed_sessions=0,
            total_sessions=10
        )
        db.session.add(patient)
        
        db.session.commit()
        print("✅ Perfiles creados")
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📝 Credenciales de acceso:")
        print("   Admin: admin / admin123")
        print("   Terapeuta: terapeuta / tera123")
        print("   Paciente: paciente / paci123")

if __name__ == '__main__':
    init_database()
