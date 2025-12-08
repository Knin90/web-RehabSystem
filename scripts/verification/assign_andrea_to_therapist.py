"""
Script para asignar a Andrea Luna (paciente original) al terapeuta
"""
from app import create_app, db
from app.models import User, Patient, Therapist, Exercise, Routine, RoutineExercise

app = create_app()

with app.app_context():
    # Obtener el terapeuta
    terapeuta = Therapist.query.first()
    if not terapeuta:
        print("❌ No se encontró ningún terapeuta")
        exit(1)
    
    # Obtener a Andrea Luna (el paciente original)
    andrea_user = User.query.filter_by(nombre_usuario='paciente').first()
    if not andrea_user:
        print("❌ No se encontró el usuario 'paciente'")
        exit(1)
    
    andrea = Patient.query.filter_by(id_usuario=andrea_user.id).first()
    if not andrea:
        print("❌ No se encontró el perfil de paciente de Andrea Luna")
        exit(1)
    
    print(f"✓ Terapeuta: {terapeuta.nombre_completo}")
    print(f"✓ Paciente: {andrea.nombre_completo}")
    
    # Verificar si ya tiene una rutina asignada
    rutina_existente = Routine.query.filter_by(
        id_terapeuta=terapeuta.id,
        id_paciente=andrea.id
    ).first()
    
    if rutina_existente:
        print(f"\n⚠ {andrea.nombre_completo} ya tiene una rutina asignada")
        print(f"   Rutina: {rutina_existente.nombre}")
        exit(0)
    
    # Obtener ejercicios
    ejercicios = Exercise.query.all()
    if not ejercicios:
        print("❌ No se encontraron ejercicios. Ejecuta seed_exercises.py primero.")
        exit(1)
    
    print(f"✓ Ejercicios disponibles: {len(ejercicios)}")
    
    # Crear rutina para Andrea
    rutina = Routine(
        nombre=f'Rutina de {andrea.nombre_completo}',
        descripcion=f'Rutina personalizada para {andrea.diagnostico}',
        id_terapeuta=terapeuta.id,
        id_paciente=andrea.id,
        duracion_minutos=30,
        dificultad='media',
        esta_activa=True
    )
    db.session.add(rutina)
    db.session.flush()
    
    print(f"\n✓ Rutina creada: {rutina.nombre}")
    
    # Agregar ejercicios a la rutina
    for idx, ejercicio in enumerate(ejercicios[:3]):
        ejercicio_rutina = RoutineExercise(
            id_rutina=rutina.id,
            id_ejercicio=ejercicio.id,
            orden=idx,
            series=3,
            repeticiones=10,
            segundos_descanso=30
        )
        db.session.add(ejercicio_rutina)
        print(f"  ✓ Ejercicio {idx+1}: {ejercicio.nombre}")
    
    db.session.commit()
    
    print("\n" + "=" * 60)
    print("✅ ANDREA LUNA ASIGNADA AL TERAPEUTA EXITOSAMENTE")
    print("=" * 60)
    
    # Verificar asignación
    print("\n🔍 Verificando asignación...")
    pacientes_asignados = terapeuta.pacientes_asignados
    print(f"\nTotal de pacientes asignados a {terapeuta.nombre_completo}: {len(pacientes_asignados)}")
    for p in pacientes_asignados:
        print(f"  - {p.nombre_completo}")
    
    print("\n✅ Ahora Andrea Luna aparecerá en la lista de pacientes del terapeuta")
