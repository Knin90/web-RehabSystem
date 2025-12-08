"""Listar TODAS las rutinas con sus ejercicios"""
from app import create_app
from app.models import Routine, Patient

app = create_app()
with app.app_context():
    routines = Routine.query.all()
    
    print(f"{'='*70}")
    print(f"TOTAL DE RUTINAS EN BD: {len(routines)}")
    print(f"{'='*70}\n")
    
    for routine in routines:
        patient_name = "TEMPLATE (sin asignar)"
        if routine.patient_id:
            patient = Patient.query.get(routine.patient_id)
            patient_name = f"{patient.full_name} (ID: {patient.id})" if patient else f"ID: {routine.patient_id}"
        
        print(f"Rutina ID: {routine.id}")
        print(f"Nombre: {routine.name}")
        print(f"Descripción: {routine.description or 'Sin descripción'}")
        print(f"Duración: {routine.duration_minutes} min")
        print(f"Dificultad: {routine.difficulty}")
        print(f"Terapeuta ID: {routine.therapist_id}")
        print(f"Paciente: {patient_name}")
        print(f"Ejercicios: {len(routine.exercises)}")
        
        if len(routine.exercises) > 0:
            for idx, ex in enumerate(routine.exercises, 1):
                if ex.exercise:
                    print(f"  {idx}. {ex.exercise.name} ({ex.sets}x{ex.repetitions}, {ex.rest_seconds}s)")
                else:
                    print(f"  {idx}. ❌ Exercise ID {ex.exercise_id} NO EXISTE")
        else:
            print("  ⚠️ SIN EJERCICIOS")
        
        print(f"{'-'*70}\n")
