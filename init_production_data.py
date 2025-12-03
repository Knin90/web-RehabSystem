"""Script para inicializar datos en producción"""
from app import create_app, db
from app.models import Exercise

def init_exercises():
    """Inicializar ejercicios si no existen"""
    app = create_app()
    with app.app_context():
        # Verificar si ya existen ejercicios
        existing_count = Exercise.query.count()
        print(f"Ejercicios existentes: {existing_count}")
        
        if existing_count >= 8:
            print("✓ Ya existen suficientes ejercicios")
            return
        
        print("Agregando ejercicios predefinidos...")
        
        exercises = [
            {'id': 1, 'name': 'Flexiones de rodilla', 'description': 'Ejercicio para fortalecer las rodillas', 'category': 'lower', 'repetitions': '3x15'},
            {'id': 2, 'name': 'Elevaciones de pierna', 'description': 'Ejercicio para fortalecer piernas', 'category': 'lower', 'repetitions': '3x12'},
            {'id': 3, 'name': 'Estiramientos lumbares', 'description': 'Ejercicio para estirar la zona lumbar', 'category': 'lower', 'repetitions': '4x30s'},
            {'id': 4, 'name': 'Rotación de hombros', 'description': 'Ejercicio para movilidad de hombros', 'category': 'upper', 'repetitions': '3x10'},
            {'id': 5, 'name': 'Flexiones de brazo', 'description': 'Ejercicio para fortalecer brazos', 'category': 'upper', 'repetitions': '3x8'},
            {'id': 6, 'name': 'Plancha abdominal', 'description': 'Ejercicio para fortalecer core', 'category': 'core', 'repetitions': '3x30s'},
            {'id': 7, 'name': 'Sentadillas asistidas', 'description': 'Ejercicio para fortalecer piernas', 'category': 'lower', 'repetitions': '3x12'},
            {'id': 8, 'name': 'Puente de glúteos', 'description': 'Ejercicio para fortalecer glúteos', 'category': 'lower', 'repetitions': '3x15'}
        ]
        
        added = 0
        for ex_data in exercises:
            # Verificar si ya existe
            existing = Exercise.query.filter_by(id=ex_data['id']).first()
            if not existing:
                exercise = Exercise(
                    id=ex_data['id'],
                    name=ex_data['name'],
                    description=ex_data['description'],
                    category=ex_data['category'],
                    repetitions=ex_data['repetitions']
                )
                db.session.add(exercise)
                added += 1
                print(f"  + {exercise.name}")
        
        if added > 0:
            db.session.commit()
            print(f"\n✅ {added} ejercicios agregados")
        else:
            print("✓ Todos los ejercicios ya existen")
        
        print(f"Total en BD: {Exercise.query.count()}")

if __name__ == '__main__':
    init_exercises()
