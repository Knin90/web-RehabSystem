"""
Script para agregar más pacientes y asignarlos al terapeuta
"""
from app import create_app, db
from app.models import User, Patient, Therapist, Exercise, Routine, RoutineExercise

app = create_app()

with app.app_context():
    # Obtener el terapeuta existente
    terapeuta = Therapist.query.first()
    if not terapeuta:
        print("❌ No se encontró ningún terapeuta. Ejecuta seed_data.py primero.")
        exit(1)
    
    print(f"✓ Terapeuta encontrado: {terapeuta.nombre_completo}")
    
    # Obtener ejercicios existentes
    ejercicios = Exercise.query.all()
    if not ejercicios:
        print("❌ No se encontraron ejercicios. Ejecuta seed_exercises.py primero.")
        exit(1)
    
    print(f"✓ Ejercicios encontrados: {len(ejercicios)}")
    
    # Lista de pacientes a crear
    pacientes_data = [
        {
            'username': 'maria_garcia',
            'email': 'maria.garcia@rehab.com',
            'password': 'maria123',
            'nombre_completo': 'María García',
            'diagnostico': 'Lesión de hombro',
            'sesiones_totales': 20,
            'sesiones_completadas': 5
        },
        {
            'username': 'juan_perez',
            'email': 'juan.perez@rehab.com',
            'password': 'juan123',
            'nombre_completo': 'Juan Pérez',
            'diagnostico': 'Rehabilitación de cadera',
            'sesiones_totales': 15,
            'sesiones_completadas': 8
        },
        {
            'username': 'carlos_rodriguez',
            'email': 'carlos.rodriguez@rehab.com',
            'password': 'carlos123',
            'nombre_completo': 'Carlos Rodríguez',
            'diagnostico': 'Lesión lumbar',
            'sesiones_totales': 18,
            'sesiones_completadas': 3
        },
        {
            'username': 'sofia_martinez',
            'email': 'sofia.martinez@rehab.com',
            'password': 'sofia123',
            'nombre_completo': 'Sofía Martínez',
            'diagnostico': 'Rehabilitación de tobillo',
            'sesiones_totales': 12,
            'sesiones_completadas': 10
        }
    ]
    
    pacientes_creados = []
    
    for paciente_data in pacientes_data:
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(nombre_usuario=paciente_data['username']).first()
        if existing_user:
            print(f"⚠ Usuario {paciente_data['username']} ya existe, saltando...")
            continue
        
        # Crear usuario
        user = User(
            nombre_usuario=paciente_data['username'],
            correo_electronico=paciente_data['email'],
            rol='patient',
            esta_activo=True
        )
        user.set_password(paciente_data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Crear perfil de paciente
        paciente = Patient(
            id_usuario=user.id,
            nombre_completo=paciente_data['nombre_completo'],
            diagnostico=paciente_data['diagnostico'],
            progreso=0.0,
            sesiones_totales=paciente_data['sesiones_totales'],
            sesiones_completadas=paciente_data['sesiones_completadas']
        )
        db.session.add(paciente)
        db.session.flush()
        
        pacientes_creados.append(paciente)
        print(f"✓ Paciente creado: {paciente.nombre_completo}")
        
        # Crear una rutina para asignar el paciente al terapeuta
        rutina = Routine(
            nombre=f'Rutina de {paciente.nombre_completo}',
            descripcion=f'Rutina personalizada para {paciente_data["diagnostico"]}',
            id_terapeuta=terapeuta.id,
            id_paciente=paciente.id,
            duracion_minutos=30,
            dificultad='media',
            esta_activa=True
        )
        db.session.add(rutina)
        db.session.flush()
        
        # Agregar 3 ejercicios aleatorios a la rutina
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
        
        print(f"  ✓ Rutina asignada con {len(ejercicios[:3])} ejercicios")
    
    db.session.commit()
    
    print("\n" + "=" * 60)
    print("✅ PACIENTES CREADOS Y ASIGNADOS EXITOSAMENTE")
    print("=" * 60)
    print(f"\nTotal de pacientes creados: {len(pacientes_creados)}")
    print(f"Todos asignados al terapeuta: {terapeuta.nombre_completo}")
    
    print("\n📝 Credenciales de los nuevos pacientes:")
    for paciente_data in pacientes_data:
        print(f"  - {paciente_data['nombre_completo']}: {paciente_data['username']} / {paciente_data['password']}")
    
    # Verificar que los pacientes estén asignados
    print("\n🔍 Verificando asignaciones...")
    pacientes_asignados = terapeuta.pacientes_asignados
    print(f"Pacientes asignados al terapeuta: {len(pacientes_asignados)}")
    for p in pacientes_asignados:
        print(f"  - {p.nombre_completo}")
