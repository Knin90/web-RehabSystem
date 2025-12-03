"""
Script de migración para agregar tablas de Rutinas
"""
from app import create_app, db
from app.models import Routine, RoutineExercise

def migrate():
    app = create_app()
    
    with app.app_context():
        print("🔄 Creando tablas de Rutinas...")
        
        try:
            # Crear las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas existen
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'routine' in tables and 'routine_exercise' in tables:
                print("✅ Verificación exitosa: tablas 'routine' y 'routine_exercise' existen")
                
                # Mostrar columnas de routine
                print("\n📋 Columnas de la tabla 'routine':")
                columns = inspector.get_columns('routine')
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
                
                # Mostrar columnas de routine_exercise
                print("\n📋 Columnas de la tabla 'routine_exercise':")
                columns = inspector.get_columns('routine_exercise')
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("❌ Error: tablas no fueron creadas")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN: Agregar tablas de Rutinas")
    print("=" * 60)
    
    if migrate():
        print("\n✅ Migración completada exitosamente")
        print("Ahora los terapeutas pueden crear y asignar rutinas a pacientes")
    else:
        print("\n❌ Migración fallida")
