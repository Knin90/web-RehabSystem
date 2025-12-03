"""Script para probar el flujo completo de rutinas"""
from app import create_app, db
from app.models import Routine, RoutineExercise, Patient, Therapist, Exercise

app = create_app()
with app.app_context():
    # Obtener terapeuta y paciente
    therapist = Therapist.query.first()
    patient = Patient.query.first()
    
    if not therapist or not patient:
        print("❌ Error: No hay terapeuta o paciente en la BD")
        exit(1)
    
    print(f"Terapeuta: {therapist.full_name} (ID: {therapist.id})")
    print(f"Paciente: {patient.full_name} (ID: {patient.id})")
    
    # Crear rutina de prueba
    print("\n1. Creando rutina de prueba...")
    routine = Routine(
        name="Rutina de Prueba",
        description="Rutina de 20 minutos para rehabilitación",
        therapist_id=therapist.id,
        duration_minutes=20,
        difficulty='medium'
    )
    db.session.add(routine)
    db.session.flush()
    print(f"   ✓ Rutina creada (ID: {routine.id})")
    
    # Agregar ejercicios a la rutina
    print("\n2. Agregando ejercicios...")
    exercises_to_add = [1, 2, 4, 6]  # IDs de ejercicios
    
    for idx, ex_id in enumerate(exercises_to_add):
        exercise = Exercise.query.get(ex_id)
        if exercise:
            routine_exercise = RoutineExercise(
                routine_id=routine.id,
                exercise_id=ex_id,
                order=idx,
                sets=3,
                repetitions=12,
                rest_seconds=30
            )
            db.session.add(routine_exercise)
            print(f"   ✓ Agregado: {exercise.name}")
        else:
            print(f"   ✗ Ejercicio ID {ex_id} no encontrado")
    
    db.session.commit()
    print(f"\n   Total ejercicios en rutina: {len(routine.exercises)}")
    
    # Asignar rutina al paciente (crear copia)
    print("\n3. Asignando rutina al paciente...")
    assigned_routine = Routine(
        name=routine.name,
        description=routine.description,
        therapist_id=routine.therapist_id,
        patient_id=patient.id,
        duration_minutes=routine.duration_minutes,
        difficulty=routine.difficulty
    )
    db.session.add(assigned_routine)
    db.session.flush()
    
    # Copiar ejercicios
    for ex in routine.exercises:
        new_exercise = RoutineExercise(
            routine_id=assigned_routine.id,
            exercise_id=ex.exercise_id,
            order=ex.order,
            sets=ex.sets,
            repetitions=ex.repetitions,
            rest_seconds=ex.rest_seconds,
            notes=ex.notes
        )
        db.session.add(new_exercise)
    
    db.session.commit()
    print(f"   ✓ Rutina asignada a {patient.full_name} (ID: {assigned_routine.id})")
    print(f"   ✓ Ejercicios copiados: {len(assigned_routine.exercises)}")
    
    # Verificar
    print("\n4. Verificando...")
    patient_routines = Routine.query.filter_by(patient_id=patient.id).all()
    print(f"   Rutinas del paciente: {len(patient_routines)}")
    
    for r in patient_routines:
        print(f"\n   Rutina: {r.name}")
        print(f"   Ejercicios: {len(r.exercises)}")
        for ex in r.exercises:
            if ex.exercise:
                print(f"     - {ex.exercise.name} ({ex.sets}x{ex.repetitions})")
    
    print("\n✅ Proceso completado exitosamente!")
    print(f"\nAhora puedes:")
    print(f"1. Iniciar sesión como paciente: {patient.user.username}")
    print(f"2. Ir a 'Mis Rutinas'")
    print(f"3. Ver la rutina '{assigned_routine.name}'")
