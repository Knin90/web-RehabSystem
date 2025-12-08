"""Verificar qué usuario está logueado y sus rutinas"""
from app import create_app
from app.models import User, Patient, Routine

app = create_app()
with app.app_context():
    # Buscar todos los usuarios pacientes
    users = User.query.filter_by(role='patient').all()
    
    print(f"{'='*70}")
    print(f"USUARIOS PACIENTES: {len(users)}")
    print(f"{'='*70}\n")
    
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        
        # Buscar perfil de paciente
        patient = Patient.query.filter_by(user_id=user.id).first()
        
        if patient:
            print(f"Patient ID: {patient.id}")
            print(f"Nombre: {patient.full_name}")
            
            # Buscar rutinas asignadas
            routines = Routine.query.filter_by(patient_id=patient.id).all()
            print(f"Rutinas asignadas: {len(routines)}")
            
            for routine in routines:
                print(f"  - Rutina ID:{routine.id} '{routine.name}' ({len(routine.exercises)} ejercicios)")
        else:
            print("❌ No tiene perfil de paciente")
        
        print(f"{'-'*70}\n")
    
    # Mostrar TODAS las rutinas
    print(f"{'='*70}")
    print("TODAS LAS RUTINAS EN BD:")
    print(f"{'='*70}\n")
    
    all_routines = Routine.query.all()
    for r in all_routines:
        print(f"ID:{r.id} '{r.name}' - Patient ID:{r.patient_id} - Ejercicios:{len(r.exercises)}")
