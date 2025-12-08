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
            
            # Crear nueva tabla con id_terapeuta nullable
            print("🔨 Creando nueva tabla...")
            cursor.execute("""
                CREATE TABLE session_capture (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_terapeuta INTEGER,
                    id_paciente INTEGER,
                    tipo_captura VARCHAR(20) NOT NULL,
                    nombre_archivo VARCHAR(255) NOT NULL,
                    ruta_archivo VARCHAR(500) NOT NULL,
                    tamano_archivo INTEGER,
                    duracion INTEGER,
                    notas TEXT,
                    fecha_sesion DATETIME,
                    fecha_creacion DATETIME,
                    es_permanente BOOLEAN DEFAULT 0,
                    contiene_audio BOOLEAN DEFAULT 0,
                    FOREIGN KEY (id_terapeuta) REFERENCES therapist(id),
                    FOREIGN KEY (id_paciente) REFERENCES patient(id)
                )
            """)
            
            # Restaurar datos existentes si los hay
            if existing_data:
                print(f"📥 Restaurando {len(existing_data)} registros...")
                # Nota: Ajustar según la estructura antigua de datos
                cursor.executemany("""
                    INSERT INTO session_capture 
                    (id, id_terapeuta, id_paciente, tipo_captura, nombre_archivo, ruta_archivo, 
                     tamano_archivo, duracion, notas, fecha_sesion, fecha_creacion, es_permanente, contiene_audio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
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
