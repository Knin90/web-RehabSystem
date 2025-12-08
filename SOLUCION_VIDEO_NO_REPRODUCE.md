# 🔧 SOLUCIÓN - VIDEO NO SE REPRODUCE

## ✅ CAMBIOS REALIZADOS

He agregado logs de debug extensivos para identificar exactamente dónde está el problema.

## 🚀 PASOS PARA DIAGNOSTICAR

### PASO 1: Verificar la ruta del archivo

```bash
python verificar_ruta_video.py
```

Este script te dirá:
- ✅ Si el archivo existe en el servidor
- ✅ La ruta exacta del archivo
- ✅ El tamaño del archivo
- ✅ La URL para acceder al archivo

### PASO 2: Reiniciar el servidor

```bash
Ctrl + C
python run.py
```

### PASO 3: Limpiar caché del navegador

```
Ctrl + Shift + R
```

O modo incógnito:
```
Ctrl + Shift + N
```

### PASO 4: Probar con logs de debug

1. **Abrir DevTools** (F12) → Console
2. **Login como paciente**: `paciente` / `paci123`
3. **Ir a**: Galería de Videos → Videos Compartidos
4. **Click en "Reproducir"**
5. **Observar la consola**

Deberías ver mensajes como:

```
🎬 DEBUG: playSharedVideoFromData llamada
  - filePath: /static/captures/video_permanente_terapeuta_2_20251207_133503.webm
  - filename: video_permanente_terapeuta_2_20251207_133503.webm
  - duration: 10
  - message: 
  - shareId: 1
  - isRead: false

🎥 DEBUG: playVideo llamada
  - filePath: /static/captures/video_permanente_terapeuta_2_20251207_133503.webm
  - filename: video_permanente_terapeuta_2_20251207_133503.webm

📹 DEBUG: Asignando src al video: /static/captures/video_permanente_terapeuta_2_20251207_133503.webm

✓ Video: loadstart
✓ Video: loadedmetadata
✓ Video: loadeddata
✓ Video: canplay
```

---

## 🐛 INTERPRETACIÓN DE LOS LOGS

### ✅ CASO 1: Todo funciona
```
✓ Video: loadstart
✓ Video: loadedmetadata
✓ Video: loadeddata
✓ Video: canplay
```
**Resultado**: El video debería reproducirse correctamente.

---

### ❌ CASO 2: Archivo no encontrado (404)
```
❌ Video error: Event {isTrusted: true, ...}
❌ Video error code: 4
❌ Video error message: MEDIA_ELEMENT_ERROR: Format error
```

**Causa**: El archivo no existe en la ruta especificada.

**Solución**:
1. Ejecuta `python verificar_ruta_video.py`
2. Verifica que el archivo existe
3. Si no existe, el terapeuta debe grabar un nuevo video

---

### ❌ CASO 3: Formato no soportado
```
❌ Video error code: 4
❌ Video error message: MEDIA_ELEMENT_ERROR: Format error
```

**Causa**: El navegador no soporta el formato WebM.

**Verificar**:
```javascript
document.createElement('video').canPlayType('video/webm')
```

**Solución**: Usa Chrome, Firefox o Edge actualizados.

---

### ❌ CASO 4: Error de permisos
```
❌ Video error code: 2
❌ Video error message: MEDIA_ELEMENT_ERROR: Network error
```

**Causa**: Problema de permisos o CORS.

**Solución**: Verifica los permisos del archivo.

---

## 🔍 VERIFICACIÓN MANUAL

### Verificar que el archivo existe:

```bash
# Windows
dir static\captures\video_permanente_terapeuta_2_20251207_133503.webm

# Linux/Mac
ls -la static/captures/video_permanente_terapeuta_2_20251207_133503.webm
```

### Verificar que el archivo es accesible:

Abre en el navegador:
```
http://localhost:5000/static/captures/video_permanente_terapeuta_2_20251207_133503.webm
```

Si el archivo se descarga o reproduce, la ruta es correcta.

---

## 📋 CÓDIGOS DE ERROR DEL VIDEO

| Código | Significado | Solución |
|--------|-------------|----------|
| 1 | MEDIA_ERR_ABORTED | Usuario canceló la carga |
| 2 | MEDIA_ERR_NETWORK | Error de red | Verificar conexión |
| 3 | MEDIA_ERR_DECODE | Error al decodificar | Archivo corrupto |
| 4 | MEDIA_ERR_SRC_NOT_SUPPORTED | Formato no soportado | Usar otro navegador |

---

## 🎯 SOLUCIONES ESPECÍFICAS

### Solución 1: Si el archivo no existe

```bash
# 1. Login como terapeuta
# 2. Ve a "Iniciar Sesión"
# 3. Graba un nuevo video
# 4. Guárdalo como permanente
# 5. Compártelo con el paciente
```

### Solución 2: Si el navegador no soporta WebM

**Navegadores compatibles**:
- ✅ Chrome 25+
- ✅ Firefox 28+
- ✅ Edge 79+
- ✅ Opera 16+
- ❌ Safari (soporte limitado)
- ❌ Internet Explorer

**Solución**: Actualiza tu navegador o usa Chrome/Firefox.

### Solución 3: Si la ruta es incorrecta

Ejecuta:
```bash
python verificar_ruta_video.py
```

Verifica la ruta en la base de datos vs. la ruta real del archivo.

---

## 🧪 PRUEBA COMPLETA EN LA CONSOLA

Copia y pega esto en la consola del navegador (F12 → Console):

```javascript
console.clear();
console.log('=== DIAGNÓSTICO DE VIDEO ===\n');

// 1. Verificar soporte de WebM
const video = document.createElement('video');
const webmSupport = video.canPlayType('video/webm');
console.log('1. Soporte de WebM:', webmSupport || 'NO SOPORTADO');

if (!webmSupport) {
    console.error('❌ Tu navegador NO soporta WebM');
    console.log('   Solución: Usa Chrome, Firefox o Edge');
}

// 2. Obtener videos compartidos
console.log('\n2. Obteniendo videos compartidos...');
fetch('/api/get-shared-videos')
    .then(r => r.json())
    .then(data => {
        console.log('   Total de videos:', data.total);
        
        if (data.videos && data.videos.length > 0) {
            const video = data.videos[0];
            console.log('\n3. Primer video:');
            console.log('   - Nombre:', video.filename);
            console.log('   - Ruta:', video.file_path);
            
            // 3. Verificar si el archivo existe
            console.log('\n4. Verificando si el archivo existe...');
            fetch(video.file_path, {method: 'HEAD'})
                .then(r => {
                    if (r.ok) {
                        console.log('   ✅ Archivo existe (Status:', r.status, ')');
                        console.log('   Content-Type:', r.headers.get('Content-Type'));
                        console.log('   Content-Length:', r.headers.get('Content-Length'), 'bytes');
                    } else {
                        console.error('   ❌ Archivo NO existe (Status:', r.status, ')');
                    }
                })
                .catch(e => console.error('   ❌ Error al verificar:', e));
        } else {
            console.log('   ⚠️ No hay videos compartidos');
        }
    })
    .catch(e => console.error('   ❌ Error en API:', e));

console.log('\n=== FIN DEL DIAGNÓSTICO ===');
```

---

## ✅ RESULTADO ESPERADO

Si todo funciona correctamente, en la consola verás:

```
🎬 DEBUG: playSharedVideoFromData llamada
  - filePath: /static/captures/video.webm
  - filename: video.webm
  ...

🎥 DEBUG: playVideo llamada
  - filePath: /static/captures/video.webm
  ...

📹 DEBUG: Asignando src al video: /static/captures/video.webm

✓ Video: loadstart
✓ Video: loadedmetadata
✓ Video: loadeddata
✓ Video: canplay
```

Y el video se reproducirá correctamente.

---

## 📞 INFORMACIÓN A PROPORCIONAR

Si el video aún no se reproduce, proporciona:

1. **Salida de** `python verificar_ruta_video.py`
2. **Logs de la consola** (todos los mensajes de DEBUG)
3. **Código de error del video** (si aparece)
4. **Resultado de la prueba completa** (código de arriba)
5. **Navegador y versión**

---

## 🎉 CONFIRMACIÓN DE ÉXITO

Si el video se reproduce correctamente:

- ✅ Modal se abre
- ✅ Video se carga (no pantalla negra)
- ✅ Duración aparece correctamente
- ✅ Controles funcionan
- ✅ Video se reproduce al hacer click en play
- ✅ No hay errores en la consola

---

**Última actualización**: Diciembre 7, 2025
**Estado**: Con logs de debug agregados ✅
