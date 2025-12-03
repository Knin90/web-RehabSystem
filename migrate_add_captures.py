"""
Script de migración para agregar la tabla SessionCapture
"""
from app import create_app, db
from app.models import SessionCapture

def migrate():
    app = create_app()
    
    with app.app_context():
        print("🔄 Creando tabla SessionCapture...")
        
        try:
            # Crear la tabla
            db.create_all()
            print("✅ Tabla SessionCapture creada exitosamente")
            
            # Verificar que la tabla existe
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'session_capture' in tables:
                print("✅ Verificación exitosa: tabla 'session_capture' existe")
                
                # Mostrar columnas
                columns = inspector.get_columns('session_capture')
                print("\n📋 Columnas de la tabla:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("❌ Error: tabla 'session_capture' no fue creada")
                
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN: Agregar tabla SessionCapture")
    print("=" * 60)
    
    if migrate():
        print("\n✅ Migración completada exitosamente")
    else:
        print("\n❌ Migración fallida")
