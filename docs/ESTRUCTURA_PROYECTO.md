# Estructura del Proyecto RehabSystem

## 📂 Organización de Carpetas

### `/app` - Aplicación Principal
Contiene el código core de la aplicación Flask:
- `__init__.py` - Inicialización de Flask y extensiones
- `config.py` - Configuraciones de la aplicación
- `models.py` - Modelos de base de datos (SQLAlchemy)
- `routes.py` - Rutas y endpoints de la API
- `forms.py` - Formularios (Flask-WTF)

### `/static` - Archivos Estáticos
Recursos del frontend:
- `css/` - Hojas de estilo personalizadas
- `js/` - Scripts JavaScript
- `images/` - Imágenes y logos
- `uploads/` - Videos y fotos de sesiones (no en Git)

### `/templates` - Plantillas HTML
Templates Jinja2 organizados por rol:
- `admin/` - Vistas de administrador
- `therapist/` - Vistas de terapeuta
- `patient/` - Vistas de paciente
- `base.html` - Template base

### `/scripts` - Scripts de Utilidad
Scripts organizados por función:

#### `/scripts/setup` - Configuración Inicial
- `setup_complete.py` ⭐ - Setup completo del sistema
- `init_db.py` - Inicializar BD vacía
- `seed_data.py` - Datos de prueba
- `seed_exercises.py` - Catálogo de ejercicios
- `seed_more_patients.py` - Más pacientes

#### `/scripts/migrations` - Migraciones de BD
- `migrate_add_captures.py` - Tabla de capturas
- `migrate_add_routines.py` - Tabla de rutinas
- `migrate_fix_therapist_nullable.py` - Fix campos

#### `/scripts/verification` - Verificación
- `verificar_sistema.py` ⭐ - Verificación completa
- `verificar_pacientes.py` - Check pacientes
- `check_routines.py` - Check rutinas
- `debug_api_patients.py` - Debug API

#### `/scripts/git` - Operaciones Git
- `git_push_codigo.bat` - Push solo código
- `git_sincronizar.bat` - Sync con GitHub
- `git_ver_cambios.bat` - Ver cambios

### `/tests` - Tests
Tests unitarios y de integración:
- `test_api_*.py` - Tests de API
- `test_auth_*.py` - Tests de autenticación
- `test_routine_*.py` - Tests de rutinas
- `test_share_*.py` - Tests de compartir videos

### `/docs` - Documentación
Documentación adicional del proyecto:
- `README.md` - Índice de documentación
- `EJECUTAR_AHORA.txt` - Guía rápida
- `COMANDOS_GIT.txt` - Comandos Git útiles
- `COMO_SUBIR_A_GITHUB.txt` - Guía de Git

### `/instance` - Base de Datos
- `rehab.db` - Base de datos SQLite (no en Git)

## 🚀 Archivos Principales en Raíz

- `run.py` - Punto de entrada de la aplicación
- `requirements.txt` - Dependencias Python
- `README.md` - Documentación principal
- `.env` - Variables de entorno (no en Git)
- `.gitignore` - Archivos ignorados por Git
- `pytest.ini` - Configuración de pytest
- `Procfile` - Config para deployment
- `render.yaml` - Config para Render

## 📝 Archivos Ignorados (.gitignore)

No se suben a GitHub:
- `.venv/` - Entorno virtual
- `__pycache__/` - Cache de Python
- `.env` - Variables de entorno
- `instance/` - Base de datos
- `static/uploads/` - Videos y fotos
- `*.log` - Logs
- `.pytest_cache/` - Cache de tests

## 🎯 Comandos Rápidos

### Configuración Inicial
```bash
python scripts/setup/setup_complete.py
```

### Ejecutar Aplicación
```bash
python run.py
```

### Verificar Sistema
```bash
python scripts/verification/verificar_sistema.py
```

### Tests
```bash
pytest
```

### Git
```bash
scripts\git\git_ver_cambios.bat
scripts\git\git_push_codigo.bat
```

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~15,000+
- **Archivos Python**: 50+
- **Templates HTML**: 30+
- **Scripts de utilidad**: 25+
- **Tests**: 20+
- **Modelos de BD**: 10

## 🔄 Flujo de Trabajo

1. **Desarrollo**: Editar código en `/app`, `/templates`, `/static`
2. **Testing**: Ejecutar tests en `/tests`
3. **Verificación**: Usar scripts en `/scripts/verification`
4. **Commit**: Usar scripts en `/scripts/git`
5. **Deployment**: Configurado en `Procfile` y `render.yaml`

## 📚 Documentación Adicional

Ver archivos en `/docs` para guías específicas y `/scripts/README.md` para documentación de scripts.
