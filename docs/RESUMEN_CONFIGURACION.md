# Resumen de Configuración Manual

## ✅ Archivos Creados

### 📖 Documentación
- `docs/CONFIGURACION_RENDER.md` - Guía completa paso a paso para Render
- `scripts/sql/README.md` - Documentación de scripts SQL

### 🗄️ Scripts SQL
- `scripts/sql/schema.sql` - Esquema completo de base de datos (10 tablas)
- `scripts/sql/seed_data.sql` - Datos iniciales (7 usuarios, 5 pacientes, 8 ejercicios)
- `scripts/sql/queries.sql` - Consultas útiles para administración

### ⚙️ Configuración
- `app/config.py` - Actualizado con soporte PostgreSQL y configuraciones de producción
- `requirements.txt` - Actualizado con gunicorn y psycopg2-binary

## 🚀 Pasos para Configurar en Render

### 1. Crear Base de Datos PostgreSQL
```
Dashboard → New + → PostgreSQL
Name: rehab-db
Database: rehab_system
User: rehab_user
Region: Oregon (US West)
```

### 2. Crear Web Service
```
Dashboard → New + → Web Service
Repository: web-RehabSystem
Branch: main
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn run:app --bind 0.0.0.0:$PORT
```

### 3. Variables de Entorno
```bash
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=<generar_clave_segura>
DATABASE_URL=<conectar_a_base_de_datos>
```

### 4. Inicializar Base de Datos

Opción A - Desde Render Shell:
```bash
python scripts/setup/setup_complete.py
```

Opción B - Usando SQL:
```bash
psql $DATABASE_URL < scripts/sql/schema.sql
psql $DATABASE_URL < scripts/sql/seed_data.sql
```

## 📊 Estructura de Base de Datos

### Tablas Creadas (10):
1. **user** - Usuarios del sistema
2. **patient** - Información de pacientes
3. **therapist** - Información de terapeutas
4. **exercise** - Catálogo de ejercicios
5. **appointment** - Citas programadas
6. **system_settings** - Configuraciones del sistema
7. **session_capture** - Fotos y videos de sesiones
8. **routine** - Rutinas de ejercicios
9. **routine_exercise** - Ejercicios en rutinas
10. **video_share** - Videos compartidos

### Datos Iniciales:
- ✅ 1 Administrador (admin / admin123)
- ✅ 1 Terapeuta (terapeuta / tera123)
- ✅ 5 Pacientes con rutinas asignadas
- ✅ 8 Ejercicios en el catálogo
- ✅ 5 Rutinas personalizadas
- ✅ 15 Ejercicios asignados a rutinas
- ✅ 12 Configuraciones del sistema

## 🔧 Comandos Útiles

### Conectar a Base de Datos:
```bash
# Desde tu computadora
psql postgresql://rehab_user:password@dpg-xxxxx-a.oregon-postgres.render.com/rehab_system

# Desde Render Shell
psql $DATABASE_URL
```

### Ejecutar Scripts SQL:
```bash
# Crear esquema
psql $DATABASE_URL < scripts/sql/schema.sql

# Insertar datos
psql $DATABASE_URL < scripts/sql/seed_data.sql

# Ejecutar consultas
psql $DATABASE_URL < scripts/sql/queries.sql
```

### Verificar Instalación:
```bash
# Desde Python
python scripts/verification/verificar_sistema.py

# Desde SQL
psql $DATABASE_URL -c "SELECT COUNT(*) FROM \"user\";"
```

## 📝 Credenciales por Defecto

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Terapeuta
- Usuario: `terapeuta`
- Contraseña: `tera123`

### Pacientes
| Usuario | Contraseña | Nombre |
|---------|------------|--------|
| paciente | paci123 | Andrea Luna |
| maria_garcia | maria123 | María García |
| juan_perez | juan123 | Juan Pérez |
| carlos_rodriguez | carlos123 | Carlos Rodríguez |
| sofia_martinez | sofia123 | Sofía Martínez |

**⚠️ IMPORTANTE**: Cambia estas contraseñas en producción!

## 🔍 Verificación

### Verificar Tablas:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

### Verificar Datos:
```sql
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

## 🐛 Solución de Problemas Comunes

### Error: "Application failed to start"
```bash
# Verificar que requirements.txt incluye:
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Error: "Database connection failed"
```bash
# Verificar DATABASE_URL en variables de entorno
# Asegurarse de usar Internal Database URL
# Verificar fix de postgres:// a postgresql://
```

### Error: "relation does not exist"
```bash
# Ejecutar esquema SQL
psql $DATABASE_URL < scripts/sql/schema.sql
```

## 📚 Documentación Completa

Ver archivos:
- `docs/CONFIGURACION_RENDER.md` - Guía detallada de Render
- `scripts/sql/README.md` - Documentación de SQL
- `README.md` - Documentación principal del proyecto

## 🎯 Próximos Pasos

1. ✅ Configurar base de datos en Render
2. ✅ Configurar web service en Render
3. ✅ Agregar variables de entorno
4. ✅ Ejecutar scripts SQL
5. ✅ Verificar deployment
6. ⚠️ Cambiar contraseñas por defecto
7. ⚠️ Configurar dominio personalizado (opcional)
8. ⚠️ Configurar backups automáticos

## 💰 Costos Estimados

### Plan Free (Desarrollo):
- Web Service: Gratis (con limitaciones)
- PostgreSQL: Gratis por 90 días, luego $7/mes
- Total: $0/mes (primeros 90 días)

### Plan Starter (Producción):
- Web Service: $7/mes
- PostgreSQL: $7/mes
- Total: $14/mes

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Consulta `docs/CONFIGURACION_RENDER.md`
4. Ejecuta `python scripts/verification/verificar_sistema.py`
5. Abre un issue en GitHub

---

**Última actualización**: Diciembre 2025
