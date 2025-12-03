"""Script para reparar rutinas vacías agregándoles ejercicios"""
from app import create_app, db
from app.models import Routine, RoutineExercise, Exercise

def fix_empty_routines():
    """Agregar ejercicios a rutinas que no tienen"""
    app = create_app()
    with app.app_context():
        # Buscar todas las rutinas
        routines = Routine.query.all()
        
        print(f"{'='*70}")
        print(f"REPARANDO RUTINAS VACÍAS")
        print(f"{'='*70}\n")
        
        fixed = 0
        
        for routine in routines:
            if len(routine.exercises) == 0:
                print(f"Rutina ID:{routine.id} '{routine.name}' - SIN EJERCICIOS")
                print(f"  Agregando ejercicios por defecto...")
                
                # Agregar 3 ejercicios por defecto según dificultad
                if routine.difficulty == 'easy':
                    exercise_ids = [1, 2, 3]  # Ejercicios fáciles
                elif routine.difficulty == 'hard':
                    exercise_ids = [5, 7, 8]  # Ejercicios difíciles
                else:
                    exercise_ids = [1, 4, 6]  # Ejercicios medios
                
                for idx, ex_id in enumerate(exercise_ids):
                    # Verificar que el ejercicio existe
                    exercise = Exercise.query.get(ex_id)
                    if exercise:
                        routine_ex = RoutineExercise(
                            routine_id=routine.id,
                            exercise_id=ex_id,
                            order=idx,
                            sets=3,
                            repetitions=12,
                            rest_seconds=30
                        )
                        db.session.add(routine_ex)
                        print(f"    + {exercise.name}")
                    else:
                        print(f"    ⚠️ Ejercicio ID {ex_id} no existe")
                
                fixed += 1
            else:
                print(f"Rutina ID:{routine.id} '{routine.name}' - ✓ Ya tiene {len(routine.exercises)} ejercicios")
        
        if fixed > 0:
            db.session.commit()
            print(f"\n✅ {fixed} rutinas reparadas")
        else:
            print(f"\n✓ Todas las rutinas ya tienen ejercicios")
        
        # Verificar resultado
        print(f"\n{'='*70}")
        print("VERIFICACIÓN FINAL:")
        print(f"{'='*70}\n")
        
        for routine in Routine.query.all():
            print(f"Rutina ID:{routine.id} '{routine.name}' - {len(routine.exercises)} ejercicios")

if __name__ == '__main__':
    fix_empty_routines()
