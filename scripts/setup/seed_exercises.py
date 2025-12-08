"""Script para agregar ejercicios predefinidos a la base de datos"""
from app import create_app, db
from app.models import Exercise

def seed_exercises():
    app = create_app()
    with app.app_context():
        # Verificar si ya existen ejercicios
        existing = Exercise.query.count()
        print(f"Ejercicios existentes: {existing}")
        
        # Lista de ejercicios predefinidos (IDs 1-8 como en el template)
        exercises = [
            {
                'id': 1,
                'nombre': 'Flexiones de rodilla',
                'descripcion': 'Ejercicio para fortalecer las rodillas',
                'categoria': 'lower',
                'repeticiones': '3x15'
            },
            {
                'id': 2,
                'nombre': 'Elevaciones de pierna',
                'descripcion': 'Ejercicio para fortalecer piernas',
                'categoria': 'lower',
                'repeticiones': '3x12'
            },
            {
                'id': 3,
                'nombre': 'Estiramientos lumbares',
                'descripcion': 'Ejercicio para estirar la zona lumbar',
                'categoria': 'lower',
                'repeticiones': '4x30s'
            },
            {
                'id': 4,
                'nombre': 'Rotación de hombros',
                'descripcion': 'Ejercicio para movilidad de hombros',
                'categoria': 'upper',
                'repeticiones': '3x10'
            },
            {
                'id': 5,
                'nombre': 'Flexiones de brazo',
                'descripcion': 'Ejercicio para fortalecer brazos',
                'categoria': 'upper',
                'repeticiones': '3x8'
            },
            {
                'id': 6,
                'nombre': 'Plancha abdominal',
                'descripcion': 'Ejercicio para fortalecer core',
                'categoria': 'core',
                'repeticiones': '3x30s'
            },
            {
                'id': 7,
                'nombre': 'Sentadillas asistidas',
                'descripcion': 'Ejercicio para fortalecer piernas',
                'categoria': 'lower',
                'repeticiones': '3x12'
            },
            {
                'id': 8,
                'nombre': 'Puente de glúteos',
                'descripcion': 'Ejercicio para fortalecer glúteos',
                'categoria': 'lower',
                'repeticiones': '3x15'
            }
        ]
        
        added = 0
        updated = 0
        
        for ex_data in exercises:
            # Verificar si el ejercicio ya existe
            exercise = Exercise.query.filter_by(id=ex_data['id']).first()
            
            if exercise:
                # Actualizar si existe
                exercise.nombre = ex_data['nombre']
                exercise.descripcion = ex_data['descripcion']
                exercise.categoria = ex_data['categoria']
                exercise.repeticiones = ex_data['repeticiones']
                updated += 1
                print(f"✓ Actualizado: {exercise.nombre}")
            else:
                # Crear nuevo
                exercise = Exercise(
                    id=ex_data['id'],
                    nombre=ex_data['nombre'],
                    descripcion=ex_data['descripcion'],
                    categoria=ex_data['categoria'],
                    repeticiones=ex_data['repeticiones']
                )
                db.session.add(exercise)
                added += 1
                print(f"+ Agregado: {exercise.nombre}")
        
        db.session.commit()
        
        print(f"\n✅ Proceso completado:")
        print(f"   - Ejercicios agregados: {added}")
        print(f"   - Ejercicios actualizados: {updated}")
        print(f"   - Total en BD: {Exercise.query.count()}")

if __name__ == '__main__':
    seed_exercises()
