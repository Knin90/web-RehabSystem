# RehabSystem - Sistema de Rehabilitación Física

Sistema web integral para la gestión de rehabilitación física que permite a terapeutas y pacientes colaborar en el proceso de recuperación mediante rutinas personalizadas, seguimiento de progreso y compartición de videos de ejercicios.

## 🌟 Características Principales

### Para Terapeutas
- **Gestión de Pacientes**: Administración completa de pacientes asignados
- **Creación de Rutinas**: Diseño de rutinas personalizadas con ejercicios específicos
- **Galería de Videos**: Captura, almacenamiento y compartición de videos de ejercicios
- **Compartir Videos**: Envío de videos instructivos a pacientes con mensajes personalizados
- **Seguimiento de Progreso**: Monitoreo del avance de cada paciente
- **Dashboard Interactivo**: Vista general de pacientes, sesiones y estadísticas

### Para Pacientes
- **Rutinas Asignadas**: Acceso a rutinas personalizadas creadas por su terapeuta
- **Galería de Videos**: Visualización de videos propios y compartidos por el terapeuta
- **Compartir Videos**: Envío de videos de progreso al terapeuta
- **Reproducción de Videos**: Player integrado con controles de velocidad y pantalla completa
- **Descarga de Videos**: Descarga de videos para visualización offline
- **Notificaciones**: Badges de videos no leídos

### Para Administradores
- **Gestión de Usuarios**: Administración de terapeutas y pacientes
- **Configuración del Sistema**: Ajustes globales de la aplicación
- **Gestión de Ejercicios**: Catálogo de ejercicios disponibles

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.1.2**: Framework web principal
- **SQLAlchemy 2.0.44**: ORM para base de datos
- **Flask-Login 0.6.3**: Gestión de autenticación
- **Flask-Bcrypt 1.0.1**: Encriptación de contraseñas
- **Flask-Migrate 4.0.5**: Migraciones de base de datos
- **Python-dotenv 1.2.1**: Gestión de variables de entorno

### Frontend
- **Bootstrap 5**: Framework CSS
- **JavaScript ES6**: Interactividad del cliente
- **HTML5 Video API**: Reproducción de videos
- **Jinja2 3.1.6**: Motor de plantillas

### Base de Datos
- **SQLite**: Base de datos en desarrollo
- Compatible con PostgreSQL para producción

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Knin90/web-RehabSystem.git
cd web-RehabSystem
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///rehab.db
```

### 5. Inicializar Base de Datos

```bash
python setup_complete.py
```

Este script creará:
- Base de datos con todas las tablas
- Usuario administrador
- Usuario terapeuta (Rafael Lu)
- 5 pacientes de prueba con rutinas asignadas
- Catálogo de 8 ejercicios
- Configuraciones del sistema

### 6. Ejecutar la Aplicación

```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 👥 Credenciales de Acceso

### Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Terapeuta
- **Usuario**: `terapeuta`
- **Contraseña**: `tera123`
- **Nombre**: Rafael Lu

### Pacientes
| Nombre | Usuario | Contraseña | Diagnóstico |
|--------|---------|------------|-------------|
| Andrea Luna | `paciente` | `paci123` | Rehabilitación rodilla |
| María García | `maria_garcia` | `maria123` | Lesión de hombro |
| Juan Pérez | `juan_perez` | `juan123` | Rehabilitación de cadera |
| Carlos Rodríguez | `carlos_rodriguez` | `carlos123` | Lesión lumbar |
| Sofía Martínez | `sofia_martinez` | `sofia123` | Rehabilitación de tobillo |

## 📁 Estructura del Proyecto

```
web-RehabSystem/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── config.py            # Configuraciones
│   ├── models.py            # Modelos de base de datos
│   └── routes.py            # Rutas y API endpoints
├── static/
│   ├── css/                 # Estilos personalizados
│   ├── js/                  # Scripts JavaScript
│   ├── images/              # Imágenes del sistema
│   └── uploads/             # Videos y capturas
├── templates/
│   ├── admin/               # Plantillas de administrador
│   ├── therapist/           # Plantillas de terapeuta
│   ├── patient/             # Plantillas de paciente
│   └── base.html            # Plantilla base
├── instance/
│   └── rehab.db             # Base de datos SQLite
├── tests/                   # Tests unitarios
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias Python
├── run.py                   # Punto de entrada
└── setup_complete.py        # Script de inicialización

```

## 🔌 API Endpoints Principales

### Autenticación
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

### Compartir Videos (Terapeuta → Paciente)
- `POST /api/share-video` - Compartir video con paciente
- `GET /api/get-patients-for-sharing` - Obtener lista de pacientes
- `GET /api/get-shared-videos` - Obtener videos compartidos (vista paciente)
- `POST /api/mark-video-as-read/<share_id>` - Marcar video como leído

### Compartir Videos (Paciente → Terapeuta)
- `POST /api/patient-share-video` - Compartir video con terapeuta
- `GET /api/get-patient-therapists` - Obtener terapeutas del paciente
- `GET /api/get-therapist-shared-videos` - Obtener videos de pacientes
- `POST /api/therapist-mark-video-as-read/<share_id>` - Marcar como leído

### Rutinas
- `GET /api/patient-routines` - Obtener rutinas del paciente
- `POST /api/create-routine` - Crear nueva rutina
- `PUT /api/update-routine/<id>` - Actualizar rutina
- `DELETE /api/delete-routine/<id>` - Eliminar rutina

## 🎥 Funcionalidades de Video

### Reproducción
- Player HTML5 integrado
- Controles de velocidad (0.5x, 1x, 1.5x, 2x)
- Modo pantalla completa
- Controles nativos (play, pause, volumen, barra de progreso)
- Autoplay al abrir modal

### Descarga
- Descarga directa de archivos
- Múltiples métodos de fallback
- Nombres de archivo descriptivos

### Compartición
- Compartir entre terapeuta y paciente (bidireccional)
- Mensajes personalizados
- Notificaciones de videos no leídos
- Marcado automático como leído al reproducir

## 🔧 Scripts Útiles

### Configuración y Datos
- `setup_complete.py` - Configuración completa del sistema
- `init_db.py` - Inicializar base de datos vacía
- `seed_data.py` - Poblar con datos de prueba
- `seed_exercises.py` - Agregar ejercicios al catálogo

### Verificación
- `verificar_sistema.py` - Verificar estado del sistema
- `verificar_pacientes.py` - Verificar pacientes asignados
- `check_routines.py` - Verificar rutinas en base de datos

### Git
- `git_push_codigo.bat` - Subir solo archivos de código
- `git_sincronizar.bat` - Sincronizar con GitHub
- `git_ver_cambios.bat` - Ver cambios pendientes

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Test específico
python test_api_simple.py
python test_shared_video_playback.py
```

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar que el entorno virtual está activado
# Windows
.venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Videos no se reproducen
- Verificar que el formato es WebM
- Limpiar caché del navegador (Ctrl+Shift+R)
- Usar modo incógnito
- Verificar que la ruta del archivo es correcta

### Pacientes no aparecen en selector
```bash
# Ejecutar script de configuración
python setup_complete.py

# Reiniciar servidor
# Ctrl+C para detener
python run.py
```

### Error de base de datos
```bash
# Reinicializar base de datos
python setup_complete.py
```

## 📝 Notas Importantes

- **Formato de Video**: Los videos deben estar en formato WebM para compatibilidad con navegadores modernos
- **Caché del Navegador**: Después de cambios en el código, limpiar caché con Ctrl+Shift+R
- **Reinicio del Servidor**: Después de cambios en Python, reiniciar con Ctrl+C y `python run.py`
- **Modo Incógnito**: Recomendado para pruebas para evitar problemas de caché

## 🚀 Despliegue en Producción

### Variables de Entorno Requeridas
```env
FLASK_ENV=production
SECRET_KEY=clave_secreta_segura
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database
PORT=5000
```

### Plataformas Compatibles
- Render
- Railway
- PythonAnywhere
- Heroku
- AWS/Azure/GCP

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado por el equipo de RehabSystem

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o solicitar features, por favor abre un issue en GitHub.

---

**Versión**: 2.0  
**Última actualización**: Diciembre 2025
