# 🧪 PRUEBA RÁPIDA - REPRODUCCIÓN Y DESCARGA

## 🎯 OBJETIVO
Verificar que las funciones de reproducir y descargar videos funcionan correctamente.

## 📋 PASOS DE PRUEBA

### PASO 1: Iniciar el servidor

```bash
python run.py
```

Espera a ver:
```
* Running on http://127.0.0.1:5000
```

---

### PASO 2: Login como Terapeuta

1. Abre el navegador: `http://localhost:5000/login`
2. Ingresa:
   - Usuario: `terapeuta`
   - Contraseña: `tera123`
3. Click en "Iniciar Sesión"

---

### PASO 3: Ir a Galería de Videos

1. En el menú lateral, click en "Galería de Videos"
2. Deberías ver una lista de videos

---

### PASO 4: Probar Reproducción

#### 4.1 Reproducir desde la tarjeta
1. Busca cualquier video en la galería
2. Click en el botón **"🎬 Reproducir"**
3. **Verificar**:
   - ✅ Se abre un modal
   - ✅ El video se carga
   - ✅ El video intenta reproducirse automáticamente
   - ✅ Puedes pausar/reproducir con los controles
   - ✅ Puedes ajustar el volumen
   - ✅ Puedes mover la barra de progreso

#### 4.2 Probar controles de velocidad
1. Con el video reproduciéndose, click en **"0.5x"**
   - ✅ El video va más lento
   - ✅ Aparece mensaje "Velocidad de reproducción: 0.5x"

2. Click en **"1x"**
   - ✅ El video vuelve a velocidad normal

3. Click en **"1.5x"**
   - ✅ El video va más rápido

4. Click en **"2x"**
   - ✅ El video va muy rápido

#### 4.3 Probar pantalla completa
1. Click en **"Pantalla completa"**
   - ✅ El video se expande a pantalla completa
   
2. Presiona `ESC` para salir
   - ✅ El video vuelve al modal

---

### PASO 5: Probar Descarga

#### 5.1 Descargar desde la tarjeta
1. En la galería, busca cualquier video
2. Click en el botón **"📥 Descargar"**
3. **Verificar**:
   - ✅ Aparece mensaje "Iniciando descarga de [nombre_archivo]"
   - ✅ El navegador inicia la descarga
   - ✅ El archivo se guarda en tu carpeta de Descargas
   - ✅ El nombre del archivo es correcto

#### 5.2 Descargar desde el modal
1. Click en **"🎬 Reproducir"** en cualquier video
2. En el modal, click en **"📥 Descargar"**
3. **Verificar**:
   - ✅ Aparece mensaje de descarga
   - ✅ El archivo se descarga correctamente

---

### PASO 6: Probar como Paciente

1. Logout (click en tu nombre → Cerrar Sesión)
2. Login como paciente:
   - Usuario: `paciente`
   - Contraseña: `paci123`
3. Ir a "Galería de Videos"
4. Repetir las pruebas de reproducción y descarga

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Reproducción:
- [ ] El modal se abre correctamente
- [ ] El video se carga
- [ ] El video intenta reproducirse automáticamente
- [ ] Los controles nativos funcionan (play, pause, volumen, barra)
- [ ] El botón 0.5x funciona
- [ ] El botón 1x funciona
- [ ] El botón 1.5x funciona
- [ ] El botón 2x funciona
- [ ] El botón de pantalla completa funciona
- [ ] Al cerrar el modal, el video se detiene

### Descarga:
- [ ] El botón de descarga en la tarjeta funciona
- [ ] El botón de descarga en el modal funciona
- [ ] Aparece el mensaje "Iniciando descarga"
- [ ] El archivo se descarga correctamente
- [ ] El nombre del archivo es correcto
- [ ] El archivo descargado se puede reproducir

### Interfaz:
- [ ] Los botones tienen iconos correctos
- [ ] Los mensajes de éxito aparecen
- [ ] El diseño es responsive
- [ ] No hay errores en la consola (F12)

---

## 🐛 PROBLEMAS COMUNES

### Problema 1: El video no se reproduce automáticamente
**Causa**: Algunos navegadores bloquean el autoplay
**Solución**: Es normal, el usuario debe hacer click en play manualmente

### Problema 2: La descarga no funciona
**Causa**: Ruta del archivo incorrecta o permisos
**Solución**: 
1. Verifica que el archivo existe en el servidor
2. Verifica los permisos de la carpeta `static/captures/`

### Problema 3: El video no se ve
**Causa**: Formato no soportado por el navegador
**Solución**: Usa formato WebM o MP4

### Problema 4: Pantalla completa no funciona
**Causa**: Navegador no soporta la API
**Solución**: Usa un navegador moderno (Chrome, Firefox, Edge)

---

## 📸 CAPTURAS ESPERADAS

### Vista de la Galería:
```
┌─────────────────────────────────────────────────────┐
│  Galería de Videos                                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  [VIDEO] │  │  [VIDEO] │  │  [VIDEO] │         │
│  │          │  │          │  │          │         │
│  │ video.webm│  │ video2.webm│ │ video3.webm│      │
│  │ 📅 Fecha  │  │ 📅 Fecha  │  │ 📅 Fecha  │       │
│  │ ⏱ 1s     │  │ ⏱ 2s     │  │ ⏱ 3s     │       │
│  │          │  │          │  │          │         │
│  │[🎬][📥]  │  │[🎬][📥]  │  │[🎬][📥]  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Modal de Reproducción:
```
┌─────────────────────────────────────────┐
│  Reproducir Video                    [X]│
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │                                   │ │
│  │         VIDEO PLAYER              │ │
│  │    ▶ ━━━━━━━━━━━━━━━ 🔊         │ │
│  │                                   │ │
│  └───────────────────────────────────┘ │
│                                         │
│  video_permanente_terapeuta_2.webm      │
│  Duración: 1 segundos                   │
│                                         │
│  [0.5x] [1x] [1.5x] [2x] [Pantalla]    │
│                                         │
├─────────────────────────────────────────┤
│  [Cerrar]              [📥 Descargar]   │
└─────────────────────────────────────────┘
```

---

## 🎯 RESULTADO ESPERADO

Después de completar todas las pruebas:

✅ **Reproducción**: Los videos se reproducen correctamente con todos los controles funcionando

✅ **Descarga**: Los videos se descargan correctamente con el nombre correcto

✅ **Interfaz**: Todo se ve bien y no hay errores en la consola

---

## 📞 SI ALGO NO FUNCIONA

1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Console"
3. Busca errores en rojo
4. Copia el error y busca ayuda

### Comandos útiles:

```bash
# Ver logs del servidor
# (en la terminal donde corre python run.py)

# Reiniciar servidor
Ctrl + C
python run.py
```

---

## ✅ PRUEBA COMPLETADA

Si todas las verificaciones pasaron, las funciones de reproducción y descarga están funcionando correctamente.

**Próximo paso**: Usar el sistema normalmente y reportar cualquier problema que encuentres.
