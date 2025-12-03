"""Crear rutina 'maria' con ejercicios"""
from app import create_app, db
from app.models import Routine, RoutineExercise, Patient, Therapist

app = create_app()
with app.app_context():
    therapist = Therapist.query.first()
    patient = Patient.query.first()
    
    if not therapist or not patient:
        print("❌ No hay terapeuta o paciente")
        exit(1)
    
    print(f"Creando rutina 'maria' para {patient.full_name}...")
    
    # Crear rutina template
    routine_template = Routine(
        name="maria",
        description="Rutina de 11 minutos",
        therapist_id=therapist.id,
        duration_minutes=11,
        difficulty='easy'
    )
    db.session.add(routine_template)
    db.session.flush()
    
    # Agregar 2 ejercicios
    exercises_ids = [1, 2]  # Flexiones de rodilla, Elevaciones de pierna
    
    for idx, ex_id in enumerate(exercises_ids):
        routine_ex = RoutineExercise(
            routine_id=routine_template.id,
            exercise_id=ex_id,
            order=idx,
            sets=3,
            repetitions=10,
            rest_seconds=30
        )
        db.session.add(routine_ex)
    
    db.session.commit()
    print(f"✓ Rutina template creada (ID: {routine_template.id})")
    
    # Asignar al paciente
    assigned_routine = Routine(
        name=routine_template.name,
        description=routine_template.description,
        therapist_id=routine_template.therapist_id,
        patient_id=patient.id,
        duration_minutes=routine_template.duration_minutes,
        difficulty=routine_template.difficulty
    )
    db.session.add(assigned_routine)
    db.session.flush()
    
    # Copiar ejercicios
    for ex in routine_template.exercises:
        new_ex = RoutineExercise(
            routine_id=assigned_routine.id,
            exercise_id=ex.exercise_id,
            order=ex.order,
            sets=ex.sets,
            repetitions=ex.repetitions,
            rest_seconds=ex.rest_seconds
        )
        db.session.add(new_ex)
    
    db.session.commit()
    
    print(f"✓ Rutina asignada a {patient.full_name} (ID: {assigned_routine.id})")
    print(f"✓ Ejercicios: {len(assigned_routine.exercises)}")
    
    for ex in assigned_routine.exercises:
        if ex.exercise:
            print(f"  - {ex.exercise.name}")
    
    print("\n✅ Listo! Ahora recarga la página del paciente")
