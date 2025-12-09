# 🔧 Fix: Paciente Puede Compartir Imágenes con Terapeutas

## 🚨 Problema

El paciente no podía compartir imágenes (snapshots) con sus terapeutas, solo videos.

**Síntoma**: El botón "Compartir con Terapeuta" solo aparecía en videos, no en imágenes.

## 🔍 Causa

El template del paciente (`video_gallery.html`) tenía una condición restrictiva que solo mostraba el botón de compartir para videos:

### Código Anterior (Restrictivo):
```javascript
${capture.type === 'video' && capture.patient_id ? `
    <button class="btn btn-warning btn-sm w-100 mt-2" onclick="shareVideoWithTherapist(${capture.id})">
        <i class="fas fa-share"></i> Compartir con Terapeuta
    </button>
` : ''}
```

**Problema**: La condición `capture.type === 'video'` excluía las imágenes.

## ✅ Solución Aplicada

Se actualizó el template del paciente para que sea consistente con el del terapeuta:

### 1. Botón de Compartir Universal

```javascript
${capture.patient_id ? `
    <button class="btn btn-warning btn-sm w-100 mt-2" onclick="shareWithTherapist(${capture.id}, '${capture.type}')">
        <i class="fas fa-share"></i> Compartir con Terapeuta
    </button>
` : ''}
```

**Cambios**:
- ✅ Removida condición `capture.type === 'video'`
- ✅ Ahora aparece para videos E imágenes
- ✅ Pasa el tipo de captura como parámetro

### 2. Modal Dinámico

```html
<h5 class="modal-title">
    <i class="fas fa-share"></i> <span id="shareModalTitle">Compartir con Terapeuta</span>
</h5>

<input type="hidden" id="shareCaptureType">

<span id="shareInfoText">Tu terapeuta recibirá una notificación...</span>

<span id="shareButtonText">Compartir</span>
```

**Cambios**:
- ✅ Título dinámico que cambia según el tipo
- ✅ Campo oculto para almacenar el tipo
- ✅ Texto informativo dinámico
- ✅ Texto del botón dinámico

### 3. Función `shareWithTherapist()`

```javascript
function shareWithTherapist(captureId, captureType) {
    document.getElementById('shareCaptureId').value = captureId;
    document.getElementById('shareCaptureType').value = captureType;
    
    // Actualizar textos del modal según el tipo
    const modalTitle = document.getElementById('shareModalTitle');
    const shareButtonText = document.getElementById('shareButtonText');
    const shareInfoText = document.getElementById('shareInfoText');
    
    if (captureType === 'video') {
        modalTitle.textContent = 'Compartir Video con Terapeuta';
        shareButtonText.textContent = 'Compartir Video';
        shareInfoText.textContent = 'Tu terapeuta recibirá una notificación y podrá ver este video.';
    } else {
        modalTitle.textContent = 'Compartir Imagen con Terapeuta';
        shareButtonText.textContent = 'Compartir Imagen';
        shareInfoText.textContent = 'Tu terapeuta recibirá una notificación y podrá ver esta imagen.';
    }
    
    loadTherapistsForSharing();
    const modal = new bootstrap.Modal(document.getElementById('shareVideoModal'));
    modal.show();
}
```

### 4. Función `confirmShare()`

```javascript
function confirmShare() {
    const captureId = document.getElementById('shareCaptureId').value;
    const captureType = document.getElementById('shareCaptureType').value;
    const therapistId = document.getElementById('shareTherapistSelect').value;
    const message = document.getElementById('shareMessage').value;
    
    const contentType = captureType === 'video' ? 'video' : 'imagen';
    
    // ... fetch a /api/patient-share-video
    
    showSuccess(`${contentType.charAt(0).toUpperCase() + contentType.slice(1)} compartido exitosamente`);
}
```

### 5. Lista de Terapeutas con Marca

```javascript
const options = data.therapists.map(therapist => {
    const tag = therapist.assigned ? ' (Asignado)' : '';
    return `<option value="${therapist.id}">${therapist.name}${tag} - ${therapist.specialty}</option>`;
});
```

## 🎯 Beneficios

### Antes:
- ❌ Solo se podían compartir videos
- ❌ Las imágenes no tenían botón de compartir
- ❌ Inconsistente con funcionalidad de terapeutas

### Ahora:
- ✅ Se pueden compartir videos E imágenes
- ✅ Modal adaptativo según tipo de contenido
- ✅ Consistente con funcionalidad de terapeutas
- ✅ Marca de terapeutas asignados
- ✅ Experiencia de usuario mejorada

## 📊 Funcionalidades Completas

### Terapeuta → Paciente:
- ✅ Compartir videos
- ✅ Compartir imágenes
- ✅ Con cualquier paciente activo
- ✅ Modal dinámico

### Paciente → Terapeuta:
- ✅ Compartir videos
- ✅ Compartir imágenes
- ✅ Con cualquier terapeuta activo
- ✅ Modal dinámico
- ✅ Marca de terapeutas asignados

**Sistema ahora es completamente simétrico** 🎉

## 🚀 Cómo Usar

### Para Pacientes:

1. **Capturar contenido**:
   - Ir a "Iniciar Terapia"
   - Capturar video o foto

2. **Compartir**:
   - Ir a "Galería de Videos"
   - Pestaña "Mis Videos"
   - Buscar video o imagen
   - Click en "Compartir con Terapeuta"
   - Seleccionar terapeuta (asignados marcados)
   - Agregar mensaje opcional
   - Click en "Compartir Video" o "Compartir Imagen"

3. **Resultado**:
   - ✅ Contenido compartido exitosamente
   - ✅ Terapeuta lo verá en "Videos de Pacientes"

## 📝 Cambios Técnicos

### Archivo Modificado:
- `templates/paciente/video_gallery.html`

### Cambios Específicos:

**1. Condición del botón**:
```diff
- ${capture.type === 'video' && capture.patient_id ? `
+ ${capture.patient_id ? `
-     onclick="shareVideoWithTherapist(${capture.id})"
+     onclick="shareWithTherapist(${capture.id}, '${capture.type}')"
```

**2. Modal**:
```diff
- <h5>Compartir Video con Terapeuta</h5>
+ <h5><span id="shareModalTitle">Compartir con Terapeuta</span></h5>

+ <input type="hidden" id="shareCaptureType">

- Tu terapeuta recibirá una notificación y podrá ver este video.
+ <span id="shareInfoText">Tu terapeuta recibirá una notificación...</span>

- <i class="fas fa-paper-plane"></i> Compartir Video
+ <i class="fas fa-paper-plane"></i> <span id="shareButtonText">Compartir</span>
```

**3. Funciones JavaScript**:
```diff
- function shareVideoWithTherapist(captureId)
+ function shareWithTherapist(captureId, captureType)

- function confirmShareVideo()
+ function confirmShare()

+ // Mantener compatibilidad
+ function shareVideoWithTherapist(captureId) {
+     shareWithTherapist(captureId, 'video');
+ }
```

## 🧪 Pruebas

### Escenario 1: Compartir imagen
- **Antes**: ❌ No había botón
- **Ahora**: ✅ Botón disponible, modal dice "Compartir Imagen"

### Escenario 2: Compartir video
- **Antes**: ✅ Funcionaba
- **Ahora**: ✅ Sigue funcionando, modal dice "Compartir Video"

### Escenario 3: Ver lista de terapeutas
- **Antes**: ❌ Solo asignados
- **Ahora**: ✅ Todos activos (asignados marcados)

## 🎨 Interfaz de Usuario

### Modal para Video:
```
┌─────────────────────────────────────┐
│ 🔗 Compartir Video con Terapeuta    │
├─────────────────────────────────────┤
│ Seleccionar Terapeuta:              │
│ [Dr. García (Asignado) - Fisio ▼]  │
│                                     │
│ Mensaje (opcional):                 │
│ [________________________]          │
│                                     │
│ ℹ️ Tu terapeuta recibirá una       │
│    notificación y podrá ver este   │
│    video.                           │
├─────────────────────────────────────┤
│ [Cancelar] [📤 Compartir Video]    │
└─────────────────────────────────────┘
```

### Modal para Imagen:
```
┌─────────────────────────────────────┐
│ 🔗 Compartir Imagen con Terapeuta   │
├─────────────────────────────────────┤
│ Seleccionar Terapeuta:              │
│ [Dra. Martínez - Rehabilitación ▼] │
│                                     │
│ Mensaje (opcional):                 │
│ [________________________]          │
│                                     │
│ ℹ️ Tu terapeuta recibirá una       │
│    notificación y podrá ver esta   │
│    imagen.                          │
├─────────────────────────────────────┤
│ [Cancelar] [📤 Compartir Imagen]   │
└─────────────────────────────────────┘
```

## ✅ Estado

- [x] Código modificado
- [x] Modal dinámico implementado
- [x] Funciones JavaScript actualizadas
- [x] Compatibilidad con código antiguo
- [x] Consistente con funcionalidad de terapeutas
- [x] Documentación creada
- [ ] Cambios subidos a GitHub
- [ ] Deploy en Render

## 🚀 Próximos Pasos

1. Subir cambios a GitHub
2. Esperar redespliegue automático en Render
3. Probar como paciente:
   - Capturar una imagen
   - Compartir con terapeuta
   - Verificar que funciona

---

**Fecha**: 8 de Diciembre, 2025
**Tipo**: Feature / Bug Fix
**Prioridad**: Alta
**Estado**: ✅ Implementado - Pendiente de deploy
**Relacionado con**: 
- FIX_COMPARTIR_CUALQUIER_PACIENTE.md
- FIX_PACIENTE_VER_TERAPEUTAS.md
- CAMBIOS_COMPARTIR_IMAGENES.md
