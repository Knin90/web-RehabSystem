"""Buscar la rutina 'smith' en la BD"""
from app import create_app
from app.models import Routine

app = create_app()
with app.app_context():
    # Buscar rutinas con nombre 'smith'
    smith_routines = Routine.query.filter(Routine.name.like('%smith%')).all()
    
    print(f"Rutinas con 'smith' en el nombre: {len(smith_routines)}")
    
    if smith_routines:
        for routine in smith_routines:
            print(f"\n{'='*60}")
            print(f"Rutina ID: {routine.id}")
            print(f"Nombre: {routine.name}")
            print(f"Paciente ID: {routine.patient_id}")
            print(f"Ejercicios: {len(routine.exercises)}")
            
            for ex in routine.exercises:
                if ex.exercise:
                    print(f"  - {ex.exercise.name}")
                else:
                    print(f"  - ❌ Exercise ID {ex.exercise_id} NO EXISTE")
    else:
        print("\n❌ No se encontró ninguna rutina 'smith'")
        print("\nRutinas disponibles:")
        all_routines = Routine.query.all()
        for r in all_routines:
            print(f"  - ID:{r.id} {r.name} (Patient:{r.patient_id}, Ejercicios:{len(r.exercises)})")
