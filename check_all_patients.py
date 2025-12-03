"""Verificar todos los pacientes y sus rutinas"""
from app import create_app
from app.models import Patient, User, Routine

app = create_app()
with app.app_context():
    patients = Patient.query.all()
    
    print(f"{'='*70}")
    print(f"TOTAL DE PACIENTES: {len(patients)}")
    print(f"{'='*70}\n")
    
    for patient in patients:
        user = User.query.get(patient.user_id)
        print(f"Paciente ID: {patient.id}")
        print(f"Nombre: {patient.full_name}")
        print(f"Usuario: {user.username if user else 'N/A'}")
        print(f"User ID: {patient.user_id}")
        
        # Rutinas asignadas
        routines = Routine.query.filter_by(patient_id=patient.id).all()
        print(f"Rutinas asignadas: {len(routines)}")
        
        for routine in routines:
            print(f"  - {routine.name} ({routine.duration_minutes} min, {len(routine.exercises)} ejercicios)")
        
        print(f"{'-'*70}\n")
