"""Script para debuggear rutinas del paciente maria"""
from app import create_app
from app.models import Routine, RoutineExercise, Patient, User, Exercise

app = create_app()
with app.app_context():
    # Buscar paciente maria
    user = User.query.filter_by(username='paciente').first()
    if not user:
        print("❌ Usuario 'paciente' no encontrado")
        exit(1)
    
    patient = Patient.query.filter_by(user_id=user.id).first()
    if not patient:
        print("❌ Perfil de paciente no encontrado")
        exit(1)
    
    print(f"Paciente: {patient.full_name} (ID: {patient.id}, User ID: {user.id})")
    
    # Buscar rutinas asignadas
    routines = Routine.query.filter_by(patient_id=patient.id).all()
    print(f"\nRutinas asignadas: {len(routines)}")
    
    for routine in routines:
        print(f"\n{'='*60}")
        print(f"Rutina ID: {routine.id}")
        print(f"Nombre: {routine.name}")
        print(f"Descripción: {routine.description}")
        print(f"Duración: {routine.duration_minutes} min")
        print(f"Dificultad: {routine.difficulty}")
        print(f"Ejercicios en relación: {len(routine.exercises)}")
        
        if len(routine.exercises) > 0:
            print(f"\nDetalles de ejercicios:")
            for idx, routine_ex in enumerate(routine.exercises):
                print(f"\n  [{idx+1}] RoutineExercise ID: {routine_ex.id}")
                print(f"      exercise_id: {routine_ex.exercise_id}")
                print(f"      order: {routine_ex.order}")
                print(f"      sets: {routine_ex.sets}")
                print(f"      repetitions: {routine_ex.repetitions}")
                print(f"      rest_seconds: {routine_ex.rest_seconds}")
                
                # Verificar si el ejercicio existe
                exercise = routine_ex.exercise
                if exercise:
                    print(f"      ✓ Exercise: {exercise.name}")
                    print(f"        Category: {exercise.category}")
                    print(f"        Description: {exercise.description}")
                else:
                    print(f"      ✗ Exercise NO ENCONTRADO (ID {routine_ex.exercise_id})")
                    # Buscar directamente
                    ex_direct = Exercise.query.get(routine_ex.exercise_id)
                    if ex_direct:
                        print(f"        Pero existe en BD: {ex_direct.name}")
                    else:
                        print(f"        No existe en tabla Exercise")
        else:
            print("  ⚠️ No hay ejercicios en esta rutina")
    
    # Verificar todos los ejercicios en BD
    print(f"\n{'='*60}")
    print("Ejercicios en BD:")
    exercises = Exercise.query.all()
    for ex in exercises:
        print(f"  {ex.id}: {ex.name}")
