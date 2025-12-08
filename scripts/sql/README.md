# Scripts SQL para RehabSystem

Esta carpeta contiene scripts SQL para crear y poblar la base de datos manualmente.

## 📁 Archivos

### `schema.sql`
Esquema completo de la base de datos con todas las tablas, índices y relaciones.

**Tablas incluidas:**
- `user` - Usuarios del sistema
- `patient` - Información de pacientes
- `therapist` - Información de terapeutas
- `exercise` - Catálogo de ejercicios
- `appointment` - Citas programadas
- `system_settings` - Configuraciones del sistema
- `session_capture` - Fotos y videos de sesiones
- `routine` - Rutinas de ejercicios
- `routine_exercise` - Ejercicios en rutinas
- `video_share` - Videos compartidos

### `seed_data.sql`
Datos iniciales para desarrollo y pruebas.

**Datos incluidos:**
- 1 Administrador
- 1 Terapeuta (Rafael Lu)
- 5 Pacientes con rutinas asignadas
- 8 Ejercicios en el catálogo
- 5 Rutinas personalizadas
- 15 Ejercicios asignados a rutinas
- 12 Configuraciones del sistema

### `queries.sql`
Consultas SQL útiles para administración y debugging.

## 🚀 Uso

### Opción 1: PostgreSQL (Producción en Render)

#### Desde tu computadora:

```bash
# Conectar a la base de datos de Render
psql postgresql://rehab_user:password@dpg-xxxxx-a.oregon-postgres.render.com/rehab_system

# Ejecutar esquema
\i scripts/sql/schema.sql

# Ejecutar datos iniciales
\i scripts/sql/seed_data.sql
```

#### Desde Render Shell:

```bash
# Abrir Shell en Render Dashboard
# Luego ejecutar:

# Opción 1: Usando psql
psql $DATABASE_URL < scripts/sql/schema.sql
psql $DATABASE_URL < scripts/sql/seed_data.sql

# Opción 2: Usando Python
python scripts/setup/setup_complete.py
```

### Opción 2: SQLite (Desarrollo Local)

```bash
# Crear base de datos
sqlite3 instance/rehab.db < scripts/sql/schema.sql
sqlite3 instance/rehab.db < scripts/sql/seed_data.sql
```

**Nota**: SQLite tiene algunas diferencias con PostgreSQL:
- `SERIAL` → `INTEGER PRIMARY KEY AUTOINCREMENT`
- `TIMESTAMP` → `DATETIME`
- Algunos `CHECK` constraints pueden no funcionar

### Opción 3: Usando Python (Recomendado)

```bash
# Ejecutar script de setup completo
python scripts/setup/setup_complete.py
```

Este script:
- Crea todas las tablas usando SQLAlchemy
- Inserta datos iniciales
- Funciona con SQLite y PostgreSQL
- Verifica la instalación

## 📊 Credenciales por Defecto

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Terapeuta
- Usuario: `terapeuta`
- Contraseña: `tera123`

### Pacientes
| Usuario | Contraseña | Nombre |
|---------|------------|--------|
| `paciente` | `paci123` | Andrea Luna |
| `maria_garcia` | `maria123` | María García |
| `juan_perez` | `juan123` | Juan Pérez |
| `carlos_rodriguez` | `carlos123` | Carlos Rodríguez |
| `sofia_martinez` | `sofia123` | Sofía Martínez |

**⚠️ IMPORTANTE**: Cambia estas contraseñas en producción!

## 🔍 Verificación

### Verificar tablas creadas:

```sql
-- PostgreSQL
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- SQLite
.tables
```

### Verificar datos:

```sql
-- Contar registros
SELECT 'Usuarios' as tabla, COUNT(*) as total FROM "user"
UNION ALL
SELECT 'Pacientes', COUNT(*) FROM patient
UNION ALL
SELECT 'Terapeutas', COUNT(*) FROM therapist
UNION ALL
SELECT 'Ejercicios', COUNT(*) FROM exercise
UNION ALL
SELECT 'Rutinas', COUNT(*) FROM routine;
```

Resultado esperado:
```
tabla      | total
-----------|------
Usuarios   | 7
Pacientes  | 5
Terapeutas | 1
Ejercicios | 8
Rutinas    | 5
```

## 🔄 Reiniciar Base de Datos

### PostgreSQL:

```bash
# Conectar a la base de datos
psql $DATABASE_URL

# Eliminar todas las tablas
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

# Recrear esquema y datos
\i scripts/sql/schema.sql
\i scripts/sql/seed_data.sql
```

### SQLite:

```bash
# Eliminar base de datos
rm instance/rehab.db

# Recrear
sqlite3 instance/rehab.db < scripts/sql/schema.sql
sqlite3 instance/rehab.db < scripts/sql/seed_data.sql
```

## 🛠️ Modificar Esquema

Si necesitas modificar el esquema:

1. Edita `schema.sql`
2. Crea un script de migración en `scripts/migrations/`
3. Ejecuta la migración:

```bash
python scripts/migrations/migrate_xxx.py
```

## 📝 Notas

### Diferencias PostgreSQL vs SQLite:

| Característica | PostgreSQL | SQLite |
|----------------|------------|--------|
| Auto-increment | `SERIAL` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Timestamp | `TIMESTAMP` | `DATETIME` |
| Boolean | `BOOLEAN` | `INTEGER (0/1)` |
| Check constraints | ✅ Soportado | ⚠️ Limitado |
| Foreign keys | ✅ Soportado | ✅ Soportado (activar con PRAGMA) |

### Contraseñas Encriptadas:

Las contraseñas en `seed_data.sql` están encriptadas con bcrypt.

Para generar nuevas contraseñas:

```python
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
password_hash = bcrypt.generate_password_hash('tu_contraseña').decode('utf-8')
print(password_hash)
```

## 🆘 Solución de Problemas

### Error: "relation does not exist"

**Causa**: Tabla no creada

**Solución**:
```bash
psql $DATABASE_URL < scripts/sql/schema.sql
```

### Error: "duplicate key value"

**Causa**: Datos ya existen

**Solución**:
```sql
-- Limpiar datos
TRUNCATE TABLE video_share, routine_exercise, routine, session_capture, 
             appointment, exercise, therapist, patient, "user", system_settings 
             CASCADE;

-- Reinsertar
\i scripts/sql/seed_data.sql
```

### Error: "permission denied"

**Causa**: Usuario sin permisos

**Solución**:
```sql
-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rehab_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rehab_user;
```

## 📚 Recursos

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
