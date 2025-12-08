# Cambios Realizados: Compartir Imágenes

## Resumen
Se agregó la funcionalidad para compartir imágenes (snapshots) entre terapeutas y pacientes, similar a como ya funcionaba con los videos.

## Cambios Realizados

### 1. Backend (routes.py)
- ✅ Actualizada la API `/api/get-shared-videos` para incluir el campo `type` (video o photo)
- ✅ Actualizada la API `/api/get-therapist-shared-videos` para incluir el campo `type`
- ✅ La API `/api/share-video` ahora funciona tanto para videos como para imágenes

### 2. Frontend - Terapeuta (video_gallery.html)
- ✅ Modificado el botón "Compartir con Paciente" para que aparezca tanto en videos como en imágenes
- ✅ Actualizado el modal de compartir para que cambie dinámicamente el título según el tipo de contenido
- ✅ Agregada función `shareWithPatient(captureId, captureType)` que maneja ambos tipos
- ✅ Actualizada función `confirmShare()` para manejar videos e imágenes
- ✅ Agregada visualización de imágenes compartidas por pacientes con botón "Ver"

### 3. Frontend - Paciente (video_gallery.html)
- ✅ Cambiado "Videos Compartidos" a "Contenido Compartido"
- ✅ Actualizada la visualización para mostrar tanto videos como imágenes
- ✅ Agregada función `viewSharedImageFromData()` para ver imágenes compartidas
- ✅ Las imágenes compartidas se marcan como leídas al visualizarlas

## Funcionalidades

### Para Terapeutas:
1. Pueden compartir tanto videos como imágenes con sus pacientes
2. El modal de compartir se adapta automáticamente al tipo de contenido
3. Pueden ver imágenes compartidas por sus pacientes

### Para Pacientes:
1. Pueden ver tanto videos como imágenes compartidas por su terapeuta
2. Las imágenes se marcan como "leídas" al visualizarlas
3. Pueden descargar tanto videos como imágenes compartidas

## Cómo Probar

### Como Terapeuta:
1. Iniciar sesión como terapeuta
2. Ir a "Galería de Videos"
3. Buscar una imagen (snapshot) en la galería
4. Hacer clic en "Compartir con Paciente"
5. Seleccionar un paciente y agregar un mensaje opcional
6. Hacer clic en "Compartir Imagen"

### Como Paciente:
1. Iniciar sesión como paciente
2. Ir a "Galería de Videos"
3. Hacer clic en la pestaña "Contenido Compartido"
4. Ver las imágenes compartidas por el terapeuta
5. Hacer clic en "Ver" para visualizar la imagen
6. La imagen se marcará como leída automáticamente

## Notas Técnicas
- El sistema reutiliza la tabla `VideoShare` para compartir tanto videos como imágenes
- El campo `tipo_captura` en `SessionCapture` determina si es 'video' o 'photo'
- La API es retrocompatible con el código existente
- Los iconos cambian automáticamente según el tipo de contenido (🎥 para videos, 📷 para fotos)

## Estado
✅ Implementación completa
✅ Compatible con funcionalidad existente
✅ Listo para pruebas
