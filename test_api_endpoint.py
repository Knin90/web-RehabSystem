"""Test del endpoint API get_routine_details"""
from app import create_app
from app.models import Routine, Patient, User
import json

app = create_app()

with app.app_context():
    # Simular request del paciente
    user = User.query.filter_by(username='paciente').first()
    patient = Patient.query.filter_by(user_id=user.id).first()
    
    print(f"Paciente: {patient.full_name} (ID: {patient.id})")
    
    # Obtener rutina
    routine = Routine.query.filter_by(patient_id=patient.id).first()
    
    if not routine:
        print("❌ No hay rutinas asignadas")
        exit(1)
    
    print(f"\nRutina: {routine.name} (ID: {routine.id})")
    print(f"Ejercicios en relación: {len(routine.exercises)}")
    
    # Simular lo que hace el endpoint
    exercises_list = []
    for routine_ex in routine.exercises:
        exercise = routine_ex.exercise
        
        # Validar que el ejercicio existe
        if not exercise:
            print(f"⚠️ Warning: Exercise ID {routine_ex.exercise_id} not found")
            continue
        
        ex_data = {
            'id': exercise.id,
            'name': exercise.name,
            'description': exercise.description or '',
            'category': exercise.category or '',
            'sets': routine_ex.sets,
            'repetitions': routine_ex.repetitions,
            'rest_seconds': routine_ex.rest_seconds,
            'notes': routine_ex.notes or '',
            'order': routine_ex.order
        }
        exercises_list.append(ex_data)
        print(f"  ✓ Agregado: {exercise.name}")
    
    # Ordenar por orden
    exercises_list.sort(key=lambda x: x['order'])
    
    # Crear respuesta como el endpoint
    response = {
        'success': True,
        'routine': {
            'id': routine.id,
            'name': routine.name,
            'description': routine.description,
            'duration_minutes': routine.duration_minutes,
            'difficulty': routine.difficulty,
            'exercises': exercises_list
        }
    }
    
    print(f"\n{'='*60}")
    print("Respuesta del endpoint simulado:")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    print(f"\nTotal ejercicios en respuesta: {len(exercises_list)}")
