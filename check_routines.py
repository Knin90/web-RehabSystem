"""Script para verificar rutinas y ejercicios asignados"""
from app import create_app
from app.models import Routine, RoutineExercise, Patient, Exercise

app = create_app()
with app.app_context():
    # Verificar paciente
    patient = Patient.query.first()
    print(f"Paciente: {patient.full_name if patient else 'None'} (ID: {patient.id if patient else 'None'})")
    
    if patient:
        # Verificar rutinas asignadas
        routines = Routine.query.filter_by(patient_id=patient.id).all()
        print(f"\nRutinas asignadas al paciente: {len(routines)}")
        
        for routine in routines:
            print(f"\n  Rutina ID:{routine.id} - {routine.name}")
            print(f"    Duración: {routine.duration_minutes} min")
            print(f"    Dificultad: {routine.difficulty}")
            print(f"    Ejercicios en relación: {len(routine.exercises)}")
            
            for ex in routine.exercises:
                exercise = ex.exercise
                if exercise:
                    print(f"      ✓ {exercise.name} (ID:{exercise.id}) - {ex.sets}x{ex.repetitions}")
                else:
                    print(f"      ✗ Exercise ID:{ex.exercise_id} NO EXISTE")
    
    # Verificar todas las rutinas
    print(f"\n{'='*60}")
    all_routines = Routine.query.all()
    print(f"Total de rutinas en BD: {len(all_routines)}")
    
    for routine in all_routines:
        print(f"\n  Rutina ID:{routine.id} - {routine.name}")
        print(f"    Terapeuta ID: {routine.therapist_id}")
        print(f"    Paciente ID: {routine.patient_id} {'(TEMPLATE)' if not routine.patient_id else '(ASIGNADA)'}")
        print(f"    Ejercicios: {len(routine.exercises)}")
    
    # Verificar ejercicios
    print(f"\n{'='*60}")
    exercises = Exercise.query.all()
    print(f"Total de ejercicios en BD: {len(exercises)}")
    for ex in exercises:
        print(f"  {ex.id}: {ex.name}")
