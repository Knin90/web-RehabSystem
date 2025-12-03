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
                'name': 'Flexiones de rodilla',
                'description': 'Ejercicio para fortalecer las rodillas',
                'category': 'lower',
                'repetitions': '3x15'
            },
            {
                'id': 2,
                'name': 'Elevaciones de pierna',
                'description': 'Ejercicio para fortalecer piernas',
                'category': 'lower',
                'repetitions': '3x12'
            },
            {
                'id': 3,
                'name': 'Estiramientos lumbares',
                'description': 'Ejercicio para estirar la zona lumbar',
                'category': 'lower',
                'repetitions': '4x30s'
            },
            {
                'id': 4,
                'name': 'Rotación de hombros',
                'description': 'Ejercicio para movilidad de hombros',
                'category': 'upper',
                'repetitions': '3x10'
            },
            {
                'id': 5,
                'name': 'Flexiones de brazo',
                'description': 'Ejercicio para fortalecer brazos',
                'category': 'upper',
                'repetitions': '3x8'
            },
            {
                'id': 6,
                'name': 'Plancha abdominal',
                'description': 'Ejercicio para fortalecer core',
                'category': 'core',
                'repetitions': '3x30s'
            },
            {
                'id': 7,
                'name': 'Sentadillas asistidas',
                'description': 'Ejercicio para fortalecer piernas',
                'category': 'lower',
                'repetitions': '3x12'
            },
            {
                'id': 8,
                'name': 'Puente de glúteos',
                'description': 'Ejercicio para fortalecer glúteos',
                'category': 'lower',
                'repetitions': '3x15'
            }
        ]
        
        added = 0
        updated = 0
        
        for ex_data in exercises:
            # Verificar si el ejercicio ya existe
            exercise = Exercise.query.filter_by(id=ex_data['id']).first()
            
            if exercise:
                # Actualizar si existe
                exercise.name = ex_data['name']
                exercise.description = ex_data['description']
                exercise.category = ex_data['category']
                exercise.repetitions = ex_data['repetitions']
                updated += 1
                print(f"✓ Actualizado: {exercise.name}")
            else:
                # Crear nuevo
                exercise = Exercise(
                    id=ex_data['id'],
                    name=ex_data['name'],
                    description=ex_data['description'],
                    category=ex_data['category'],
                    repetitions=ex_data['repetitions']
                )
                db.session.add(exercise)
                added += 1
                print(f"+ Agregado: {exercise.name}")
        
        db.session.commit()
        
        print(f"\n✅ Proceso completado:")
        print(f"   - Ejercicios agregados: {added}")
        print(f"   - Ejercicios actualizados: {updated}")
        print(f"   - Total en BD: {Exercise.query.count()}")

if __name__ == '__main__':
    seed_exercises()
