# Scripts de Utilidad

Esta carpeta contiene scripts organizados por categoría para facilitar el desarrollo y mantenimiento del proyecto.

## Estructura

### setup/
Scripts para configuración inicial y población de datos:
- `setup_complete.py` - Configuración completa del sistema
- `init_db.py` - Inicializar base de datos
- `seed_data.py` - Poblar con datos de prueba
- `seed_exercises.py` - Agregar ejercicios
- `seed_more_patients.py` - Agregar más pacientes

### migrations/
Scripts de migración de base de datos:
- `migrate_add_captures.py` - Agregar tabla de capturas
- `migrate_add_routines.py` - Agregar tabla de rutinas
- `migrate_fix_therapist_nullable.py` - Corregir campos nullable

### verification/
Scripts para verificar el estado del sistema:
- `verificar_sistema.py` - Verificación completa del sistema
- `verificar_pacientes.py` - Verificar pacientes asignados
- `check_routines.py` - Verificar rutinas
- `debug_api_patients.py` - Debug de API de pacientes

### git/
Scripts para operaciones de Git:
- `git_push_codigo.bat` - Subir solo código
- `git_sincronizar.bat` - Sincronizar con GitHub
- `git_ver_cambios.bat` - Ver cambios pendientes

## Uso

Ejecutar desde la raíz del proyecto:

```bash
# Configuración inicial
python scripts/setup/setup_complete.py

# Verificar sistema
python scripts/verification/verificar_sistema.py

# Git operations
scripts/git/git_ver_cambios.bat
```
