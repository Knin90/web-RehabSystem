"""
Script de migración para hacer therapist_id nullable en SessionCapture
"""
from app import create_app, db
from app.models import SessionCapture
import sqlite3

def migrate():
    app = create_app()
    
    with app.app_context():
        print("🔄 Modificando tabla SessionCapture...")
        
        try:
            # Obtener la ruta de la base de datos
            db_path = 'instance/rehab.db'
            
            # Conectar directamente con sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar si la tabla existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='session_capture'")
            if not cursor.fetchone():
                print("❌ Tabla session_capture no existe. Ejecuta migrate_add_captures.py primero.")
                conn.close()
                return False
            
            print("📋 Tabla session_capture encontrada")
            
            # Obtener datos existentes
            cursor.execute("SELECT * FROM session_capture")
            existing_data = cursor.fetchall()
            print(f"📊 Registros existentes: {len(existing_data)}")
            
            # Eliminar tabla antigua
            print("🗑️ Eliminando tabla antigua...")
            cursor.execute("DROP TABLE IF EXISTS session_capture")
            
            # Crear nueva tabla con therapist_id nullable
            print("🔨 Creando nueva tabla...")
            cursor.execute("""
                CREATE TABLE session_capture (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    therapist_id INTEGER,
                    patient_id INTEGER,
                    capture_type VARCHAR(20) NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    file_size INTEGER,
                    duration INTEGER,
                    notes TEXT,
                    session_date DATETIME,
                    created_at DATETIME,
                    FOREIGN KEY (therapist_id) REFERENCES therapist(id),
                    FOREIGN KEY (patient_id) REFERENCES patient(id)
                )
            """)
            
            # Restaurar datos existentes si los hay
            if existing_data:
                print(f"📥 Restaurando {len(existing_data)} registros...")
                cursor.executemany("""
                    INSERT INTO session_capture 
                    (id, therapist_id, patient_id, capture_type, filename, file_path, 
                     file_size, duration, notes, session_date, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, existing_data)
            
            conn.commit()
            conn.close()
            
            print("✅ Migración completada exitosamente")
            print("✅ therapist_id ahora es nullable")
            
            # Verificar con SQLAlchemy
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('session_capture')
            print("\n📋 Columnas actualizadas:")
            for col in columns:
                nullable = "NULL" if col.get('nullable', True) else "NOT NULL"
                print(f"  - {col['name']}: {col['type']} ({nullable})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN: Hacer therapist_id nullable en SessionCapture")
    print("=" * 60)
    
    if migrate():
        print("\n✅ Migración completada exitosamente")
        print("Ahora los pacientes pueden guardar capturas sin terapeuta asociado")
    else:
        print("\n❌ Migración fallida")
