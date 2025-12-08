# 💾 Guía de Almacenamiento - Fotos y Videos

## 🎯 Descripción

El sistema ahora permite **guardar fotos y videos** de las sesiones de rehabilitación directamente en el servidor, con almacenamiento en base de datos y archivos físicos.

---

## ✨ Nuevas Funcionalidades

### 1. 📸 Guardar Fotos
- Captura instantáneas de la sesión
- Almacenamiento automático en el servidor
- Asociación con terapeuta y paciente
- Notas opcionales

### 2. 🎥 Grabar Videos
- Grabación de sesiones completas
- Formato WebM (compatible con todos los navegadores)
- Duración automática
- Almacenamiento en servidor

### 3. 📂 Ver Capturas Guardadas
- Lista de todas las capturas
- Filtrado por tipo (foto/video)
- Visualización directa
- Información detallada (tamaño, fecha, etc.)

---

## 🗄️ Estructura de Almacenamiento

### Base de Datos

**Tabla:** `session_capture`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID único |
| `therapist_id` | Integer | ID del terapeuta |
| `patient_id` | Integer | ID del paciente (opcional) |
| `capture_type` | String | 'photo' o 'video' |
| `filename` | String | Nombre del archivo |
| `file_path` | String | Ruta completa del archivo |
| `file_size` | Integer | Tamaño en bytes |
| `duration` | Integer | Duración en segundos (solo videos) |
| `notes` | Text | Notas del terapeuta |
| `session_date` | DateTime | Fecha de la sesión |
| `created_at` | DateTime | Fecha de creación |

### Sistema de Archivos

```
static/
└── uploads/
    ├── photos/
    │   ├── snapshot_1_20241202_195530.jpg
    │   ├── snapshot_1_20241202_195645.jpg
    │   └── ...
    └── videos/
        ├── video_1_20241202_195730.webm
        ├── video_1_20241202_200015.webm
        └── ...
```

**Nomenclatura:**
- Fotos: `snapshot_{user_id}_{timestamp}.jpg`
- Videos: `video_{user_id}_{timestamp}.webm`

---

## 🚀 Cómo Usar

### Capturar y Guardar Foto

1. **Iniciar cámara**
   - Hacer clic en "Iniciar Cámara"

2. **Capturar foto**
   - Hacer clic en "Capturar Foto"
   - La foto se guarda automáticamente en el servidor

3. **Agregar notas (opcional)**
   - Escribir observaciones en el área de notas
   - Las notas se asocian con la captura

4. **Confirmación**
   - Aparece notificación: "✅ Foto guardada: snapshot_xxx.jpg"

### Grabar y Guardar Video

1. **Iniciar cámara**
   - Hacer clic en "Iniciar Cámara"

2. **Iniciar grabación**
   - Hacer clic en "Grabar Video"
   - Aparece indicador "REC" en rojo

3. **Detener grabación**
   - Hacer clic en "Detener Grabación"
   - El video se guarda automáticamente

4. **Confirmación**
   - Aparece notificación: "✅ Video guardado: video_xxx.webm (30s)"

### Ver Capturas Guardadas

1. **Abrir galería**
   - Hacer clic en "Ver Capturas"

2. **Explorar**
   - Ver lista de todas las capturas
   - Información: tipo, nombre, tamaño, fecha

3. **Visualizar**
   - Hacer clic en "Ver" para abrir la captura
   - Se abre en nueva pestaña

---

## 🔧 API Endpoints

### POST `/api/save-snapshot`

Guardar foto capturada.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "patient_id": 1,
  "notes": "Buena postura en ejercicio de rodilla"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Foto guardada correctamente",
  "filename": "snapshot_1_20241202_195530.jpg",
  "file_size": 245678,
  "capture_id": 1
}
```

### POST `/api/save-video`

Guardar video grabado.

**Request (FormData):**
- `video`: Archivo de video (Blob)
- `patient_id`: ID del paciente
- `notes`: Notas opcionales
- `duration`: Duración en segundos

**Response:**
```json
{
  "success": true,
  "message": "Video guardado correctamente",
  "filename": "video_1_20241202_195730.webm",
  "file_size": 1234567,
  "duration": 30,
  "capture_id": 2
}
```

### GET `/api/get-captures`

Obtener lista de capturas del terapeuta.

**Response:**
```json
{
  "success": true,
  "captures": [
    {
      "id": 1,
      "type": "photo",
      "filename": "snapshot_1_20241202_195530.jpg",
      "file_path": "static/uploads/photos/snapshot_1_20241202_195530.jpg",
      "file_size": 245678,
      "duration": null,
      "notes": "Buena postura",
      "patient_id": 1,
      "created_at": "2024-12-02 19:55:30"
    },
    {
      "id": 2,
      "type": "video",
      "filename": "video_1_20241202_195730.webm",
      "file_path": "static/uploads/videos/video_1_20241202_195730.webm",
      "file_size": 1234567,
      "duration": 30,
      "notes": "",
      "patient_id": 1,
      "created_at": "2024-12-02 19:57:30"
    }
  ],
  "total": 2
}
```

---

## 📊 Especificaciones Técnicas

### Fotos

| Especificación | Valor |
|----------------|-------|
| Formato | JPEG |
| Calidad | 80% |
| Resolución | 1280x720 (HD) |
| Tamaño promedio | 200-300 KB |
| Codificación | Base64 → Binary |

### Videos

| Especificación | Valor |
|----------------|-------|
| Formato | WebM |
| Codec | VP9 |
| Resolución | 1280x720 (HD) |
| Frame rate | 30 FPS |
| Tamaño promedio | 1-2 MB por minuto |

---

## 🔒 Seguridad

### Validaciones

1. **Autenticación**
   - Solo terapeutas autenticados pueden guardar
   - Verificación de rol con `@role_required('therapist')`

2. **Validación de datos**
   - Verificación de formato de imagen
   - Validación de tamaño de archivo
   - Sanitización de nombres de archivo

3. **Almacenamiento seguro**
   - Nombres de archivo únicos (timestamp)
   - Carpetas con permisos restringidos
   - No se sobrescriben archivos existentes

### Privacidad

- ✅ Solo el terapeuta que creó la captura puede verla
- ✅ Asociación con paciente para trazabilidad
- ✅ Notas encriptadas en base de datos
- ✅ Archivos no accesibles públicamente sin autenticación

---

## 💾 Gestión de Espacio

### Tamaños Estimados

**Por sesión (30 minutos):**
- 5 fotos: ~1.5 MB
- 1 video: ~30 MB
- **Total:** ~31.5 MB

**Por mes (100 sesiones):**
- Fotos: ~150 MB
- Videos: ~3 GB
- **Total:** ~3.15 GB

### Recomendaciones

1. **Limpieza periódica**
   - Eliminar capturas antiguas (> 6 meses)
   - Archivar capturas importantes

2. **Monitoreo de espacio**
   - Verificar espacio disponible regularmente
   - Alertas cuando quede < 10% de espacio

3. **Backup**
   - Respaldar capturas semanalmente
   - Almacenar en servicio de nube (AWS S3, Google Cloud)

---

## 🛠️ Mantenimiento

### Migración de Base de Datos

Para agregar la tabla `session_capture`:

```bash
python migrate_add_captures.py
```

### Verificar Integridad

```python
from app import create_app, db
from app.models import SessionCapture
import os

app = create_app()
with app.app_context():
    captures = SessionCapture.query.all()
    
    for capture in captures:
        if not os.path.exists(capture.file_path):
            print(f"❌ Archivo faltante: {capture.filename}")
        else:
            print(f"✅ OK: {capture.filename}")
```

### Limpiar Archivos Huérfanos

```python
import os
from app import create_app, db
from app.models import SessionCapture

app = create_app()
with app.app_context():
    # Obtener todos los archivos en uploads
    photos_dir = 'static/uploads/photos'
    videos_dir = 'static/uploads/videos'
    
    all_files = []
    all_files.extend([os.path.join(photos_dir, f) for f in os.listdir(photos_dir)])
    all_files.extend([os.path.join(videos_dir, f) for f in os.listdir(videos_dir)])
    
    # Obtener archivos en BD
    db_files = [c.file_path for c in SessionCapture.query.all()]
    
    # Encontrar huérfanos
    orphans = [f for f in all_files if f not in db_files]
    
    print(f"Archivos huérfanos: {len(orphans)}")
    for orphan in orphans:
        print(f"  - {orphan}")
        # os.remove(orphan)  # Descomentar para eliminar
```

---

## 📈 Estadísticas

### Consultas Útiles

**Total de capturas por terapeuta:**
```python
from app.models import SessionCapture, Therapist

therapist = Therapist.query.filter_by(user_id=current_user.id).first()
total_photos = SessionCapture.query.filter_by(
    therapist_id=therapist.id, 
    capture_type='photo'
).count()
total_videos = SessionCapture.query.filter_by(
    therapist_id=therapist.id, 
    capture_type='video'
).count()

print(f"Fotos: {total_photos}, Videos: {total_videos}")
```

**Espacio total usado:**
```python
from app.models import SessionCapture
from sqlalchemy import func

total_size = db.session.query(
    func.sum(SessionCapture.file_size)
).scalar() or 0

print(f"Espacio usado: {total_size / (1024**2):.2f} MB")
```

---

## 🐛 Troubleshooting

### Error: "No se recibió imagen"

**Causa:** El formato de la imagen no es correcto

**Solución:**
- Verificar que la imagen esté en formato base64
- Verificar que tenga el prefijo `data:image/jpeg;base64,`

### Error: "Terapeuta no encontrado"

**Causa:** El usuario no tiene perfil de terapeuta

**Solución:**
```python
from app.models import Therapist
therapist = Therapist(
    user_id=current_user.id,
    full_name=current_user.username,
    specialty='General'
)
db.session.add(therapist)
db.session.commit()
```

### Error: "Permission denied" al guardar archivo

**Causa:** Permisos insuficientes en carpeta uploads

**Solución:**
```bash
# Linux/Mac
chmod 755 static/uploads
chmod 755 static/uploads/photos
chmod 755 static/uploads/videos

# Windows
# Dar permisos de escritura a la carpeta en Propiedades
```

---

## 📚 Recursos Adicionales

- [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [File API](https://developer.mozilla.org/en-US/docs/Web/API/File)

---

**Última actualización:** Diciembre 2, 2024  
**Versión:** 2.2.0  
**Autor:** Denis - RehabSystem Team

---

¡Ahora puedes guardar y gestionar todas las capturas de tus sesiones! 📸🎥
