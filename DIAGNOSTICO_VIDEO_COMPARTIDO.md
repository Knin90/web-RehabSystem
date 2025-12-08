# 🔍 DIAGNÓSTICO - VIDEO COMPARTIDO NO SE REPRODUCE

## ❌ PROBLEMA
El video compartido por el terapeuta no se puede reproducir en el lado del paciente.

## 🧪 PASO 1: Verificar que hay videos compartidos

```bash
python test_shared_video_playback.py
```

Este script verifica:
- ✅ Si el paciente existe
- ✅ Si hay videos compartidos
- ✅ Si los archivos de video existen
- ✅ La respuesta de la API

---

## 🔍 PASO 2: Verificar en el navegador

### 2.1 Abrir DevTools
1. Presiona **F12**
2. Ve a la pestaña **Console**

### 2.2 Login como paciente
```
Usuario: paciente
Contraseña: paci123
```

### 2.3 Ir a Videos Compartidos
1. Click en "Galería de Videos"
2. Click en la pestaña "Videos Compartidos"

### 2.4 Observar la consola
Deberías ver mensajes como:
```
Cargando videos compartidos...
Respuesta de API: {success: true, videos: Array(1), total: 1}
```

---

## 🐛 ERRORES COMUNES

### Error 1: "playSharedVideoFromData is not defined"

**Causa**: La función JavaScript no se cargó

**Solución**:
```bash
# Reiniciar servidor
Ctrl + C
python run.py

# Limpiar caché
Ctrl + Shift + R
```

---

### Error 2: "404 Not Found" al cargar el video

**Causa**: El archivo de video no existe

**Verificar**:
```bash
# Ver si el archivo existe
dir static\captures\*.webm
```

**Solución**: El terapeuta debe grabar un nuevo video

---

### Error 3: El video no se reproduce (sin errores)

**Causa**: El navegador no soporta el formato WebM

**Verificar**:
1. Abre la consola (F12)
2. Escribe:
```javascript
document.createElement('video').canPlayType('video/webm')
```

**Resultado esperado**: `"probably"` o `"maybe"`

Si dice `""` (vacío), tu navegador no soporta WebM.

**Solución**: Usa Chrome, Firefox o Edge (versiones recientes)

---

### Error 4: "Cannot read property 'getAttribute' of null"

**Causa**: El botón no tiene los atributos `data-*`

**Verificar**:
1. Click derecho en el botón "Reproducir" → Inspeccionar
2. Deberías ver:
```html
<button data-filepath="/static/captures/video.webm" 
        data-filename="video.webm" 
        data-duration="5" 
        data-message=""
        data-shareid="1"
        data-isread="false"
        onclick="playSharedVideoFromData(this)">
```

Si NO tiene `data-*`, el servidor no se reinició.

---

## 🧪 PASO 3: Probar manualmente en la consola

Abre la consola del navegador (F12 → Console) y ejecuta:

```javascript
// Verificar que las funciones existen
console.log('playSharedVideoFromData:', typeof playSharedVideoFromData);
console.log('playVideo:', typeof playVideo);
```

**Resultado esperado**:
```
playSharedVideoFromData: function
playVideo: function
```

---

```javascript
// Probar reproducir un video manualmente
playVideo('/static/captures/video_test.webm', 'video_test.webm', 5, 'Test')
```

**Resultado esperado**: Se abre el modal con el video

---

## 🔧 PASO 4: Verificar la ruta del video

En la consola:

```javascript
// Ver los videos compartidos
fetch('/api/get-shared-videos')
    .then(r => r.json())
    .then(data => {
        console.log('Videos compartidos:', data);
        if (data.videos && data.videos.length > 0) {
            const video = data.videos[0];
            console.log('Primer video:');
            console.log('  - Ruta:', video.file_path);
            console.log('  - Nombre:', video.filename);
            
            // Verificar si el archivo existe
            fetch(video.file_path)
                .then(r => console.log('Archivo existe:', r.status === 200))
                .catch(e => console.log('Error:', e));
        }
    });
```

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [ ] Ejecuté `python test_shared_video_playback.py`
- [ ] Vi que hay videos compartidos
- [ ] Los archivos de video existen
- [ ] Reinicié el servidor Flask
- [ ] Limpié el caché del navegador (Ctrl+Shift+R)
- [ ] Abrí DevTools (F12) → Console
- [ ] Login como paciente
- [ ] Fui a "Videos Compartidos"
- [ ] No hay errores en rojo en la consola
- [ ] `typeof playSharedVideoFromData` devuelve `"function"`
- [ ] Los botones tienen atributos `data-*`
- [ ] El navegador soporta WebM

---

## 🎯 SOLUCIONES ESPECÍFICAS

### Solución 1: Si no hay videos compartidos

```bash
# 1. Login como terapeuta
# 2. Ve a Galería de Videos
# 3. Click en "Compartir con Paciente" en un video
# 4. Selecciona al paciente
# 5. Escribe un mensaje (opcional)
# 6. Click en "Compartir Video"
```

---

### Solución 2: Si el archivo no existe

El terapeuta debe grabar un nuevo video:
```bash
# 1. Login como terapeuta
# 2. Ve a "Iniciar Sesión"
# 3. Graba un video
# 4. Guárdalo como permanente
# 5. Compártelo con el paciente
```

---

### Solución 3: Si el navegador no soporta WebM

Opciones:
1. Usa Chrome, Firefox o Edge (versiones recientes)
2. O convierte el video a MP4 (requiere cambios en el código)

---

### Solución 4: Si las funciones no están definidas

```bash
# 1. Detener servidor
Ctrl + C

# 2. Reiniciar
python run.py

# 3. Limpiar caché
Ctrl + Shift + R

# 4. O usar modo incógnito
Ctrl + Shift + N
```

---

## 🧪 PRUEBA COMPLETA

Ejecuta esto en la consola del navegador (F12 → Console):

```javascript
console.clear();
console.log('=== DIAGNÓSTICO COMPLETO ===\n');

// 1. Verificar funciones
console.log('1. Funciones JavaScript:');
console.log('  playSharedVideoFromData:', typeof playSharedVideoFromData);
console.log('  playVideo:', typeof playVideo);
console.log('  downloadFile:', typeof downloadFile);

// 2. Verificar elementos DOM
console.log('\n2. Elementos DOM:');
console.log('  videoModal:', !!document.getElementById('videoModal'));
console.log('  modalVideo:', !!document.getElementById('modalVideo'));
console.log('  sharedVideoGallery:', !!document.getElementById('sharedVideoGallery'));

// 3. Verificar botones
const playButtons = document.querySelectorAll('button[onclick*="playSharedVideoFromData"]');
console.log('\n3. Botones:');
console.log('  Botones de reproducir:', playButtons.length);

if (playButtons.length > 0) {
    const firstButton = playButtons[0];
    console.log('  Primer botón tiene data-filepath:', !!firstButton.getAttribute('data-filepath'));
    console.log('  Primer botón tiene data-filename:', !!firstButton.getAttribute('data-filename'));
}

// 4. Verificar soporte de WebM
const video = document.createElement('video');
const webmSupport = video.canPlayType('video/webm');
console.log('\n4. Soporte de formato:');
console.log('  WebM:', webmSupport || 'NO SOPORTADO');

// 5. Verificar API
console.log('\n5. Verificando API...');
fetch('/api/get-shared-videos')
    .then(r => r.json())
    .then(data => {
        console.log('  API funciona:', data.success);
        console.log('  Total de videos:', data.total);
        if (data.videos && data.videos.length > 0) {
            console.log('  Primer video:', data.videos[0].filename);
            console.log('  Ruta:', data.videos[0].file_path);
        }
    })
    .catch(e => console.log('  Error en API:', e));

console.log('\n=== FIN DEL DIAGNÓSTICO ===');
```

Copia el resultado completo.

---

## 📞 INFORMACIÓN A PROPORCIONAR

Si nada funciona, proporciona:

1. **Salida de** `python test_shared_video_playback.py`
2. **Resultado del diagnóstico completo** (código de arriba)
3. **Captura de la consola** cuando intentas reproducir
4. **HTML del botón** (click derecho → Inspeccionar)
5. **Navegador y versión**

---

## ✅ RESULTADO ESPERADO

Si todo funciona correctamente:

1. **Click en "Reproducir"** en un video compartido:
   - ✅ Se abre el modal
   - ✅ El video se carga
   - ✅ El video se reproduce
   - ✅ Se marca como leído
   - ✅ El badge "Nuevo" desaparece

2. **En la consola**:
   - ✅ No hay errores en rojo
   - ✅ Se ven los logs de debug
   - ✅ La API devuelve los videos

---

**Última actualización**: Diciembre 6, 2025
