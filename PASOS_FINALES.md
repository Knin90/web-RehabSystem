# 🎯 PASOS FINALES - Ver Pacientes en el Selector

**Estado Actual:** ✅ Los pacientes están en la base de datos  
**Verificado:** ✅ La API devuelve 5 pacientes correctamente  
**Falta:** Reiniciar el servidor y probar en el navegador

---

## ✅ PASO 1: Reiniciar el Servidor Flask

### Si el servidor está corriendo:

1. **Ve a la terminal donde está corriendo el servidor**
2. **Presiona:** `Ctrl + C`
3. **Espera a que se detenga completamente**

### Iniciar el servidor nuevamente:

```bash
python run.py
```

**Deberías ver:**
```
 * Serving Flask app 'app'
 * Debug mode: on/off
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

✅ **El servidor está listo**

---

## ✅ PASO 2: Abrir Navegador en Modo Incógnito

**¿Por qué modo incógnito?**
- Evita problemas de caché
- Sesión limpia
- Sin cookies antiguas

### Cómo abrir modo incógnito:

- **Chrome:** `Ctrl + Shift + N`
- **Firefox:** `Ctrl + Shift + P`
- **Edge:** `Ctrl + Shift + N`

---

## ✅ PASO 3: Login como Terapeuta

1. **Ir a:** http://localhost:5000

2. **Login:**
   - Usuario: `terapeuta`
   - Contraseña: `tera123`

3. **Click en "Iniciar Sesión"**

✅ **Deberías ver el dashboard del terapeuta**

---

## ✅ PASO 4: Ir a Galería de Videos

1. **En el menú lateral, click en:** "Galería de Videos"

2. **Deberías ver la página de galería**

---

## ✅ PASO 5: Intentar Compartir un Video

1. **Si no hay videos, eso es normal**
   - La funcionalidad de compartir sigue funcionando

2. **Busca cualquier video (o crea uno de prueba)**

3. **Click en el botón:** "Compartir con Paciente"

4. **Se abrirá un modal**

---

## 🎯 RESULTADO ESPERADO

Deberías ver este selector:

```
┌─────────────────────────────────────┐
│ Seleccionar Paciente:               │
│ ┌─────────────────────────────────┐ │
│ │ Selecciona un paciente...       │ │ ← Click aquí
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

Al hacer click, deberías ver:

┌─────────────────────────────────────┐
│ Selecciona un paciente...           │
│ Andrea Luna - Rehabilitación rodilla│
│ María García - Lesión de hombro     │
│ Juan Pérez - Rehabilitación de...   │
│ Carlos Rodríguez - Lesión lumbar    │
│ Sofía Martínez - Rehabilitación...  │
└─────────────────────────────────────┘
```

✅ **Si ves los 5 pacientes, ¡FUNCIONA!**

---

## 🐛 Si AÚN No Aparecen los Pacientes

### Verificación 1: Abrir DevTools

1. **Presiona:** `F12`
2. **Ve a la pestaña:** "Console"
3. **Busca errores en rojo**

**Si ves errores:**
- Copia el error completo
- Busca en el código

### Verificación 2: Ver la Petición de Red

1. **Con DevTools abierto (F12)**
2. **Ve a la pestaña:** "Network"
3. **Intenta compartir un video nuevamente**
4. **Busca la petición:** `get-patients-for-sharing`
5. **Click en ella**
6. **Ve a la pestaña "Response"**

**Deberías ver:**
```json
{
  "success": true,
  "patients": [
    {"id": 1, "name": "Andrea Luna", "diagnosis": "Rehabilitación rodilla"},
    {"id": 2, "name": "María García", "diagnosis": "Lesión de hombro"},
    ...
  ],
  "total": 5
}
```

**Si ves `"total": 0`:**
- El servidor no se reinició correctamente
- Detén el servidor (`Ctrl + C`)
- Ejecuta: `python setup_complete.py`
- Inicia el servidor: `python run.py`

**Si ves un error 302 o redirect:**
- No estás logueado correctamente
- Cierra el navegador
- Abre modo incógnito nuevamente
- Login como terapeuta

**Si ves un error 500:**
- Hay un error en el servidor
- Mira la terminal del servidor
- Copia el error completo

### Verificación 3: Probar la API Directamente

**En el navegador, ve a:**
```
http://localhost:5000/api/get-patients-for-sharing
```

**Si ves un redirect a login:**
- Es normal, necesitas estar logueado

**Para probar sin navegador:**
```bash
python test_browser_simulation.py
```

**Deberías ver:**
```
✅ Total de pacientes: 5

👥 PACIENTES QUE DEBERÍAN APARECER EN EL SELECTOR:
   1. Andrea Luna - Rehabilitación rodilla
   2. María García - Lesión de hombro
   3. Juan Pérez - Rehabilitación de cadera
   4. Carlos Rodríguez - Lesión lumbar
   5. Sofía Martínez - Rehabilitación de tobillo
```

---

## 📋 Checklist Completo

Antes de reportar que no funciona, verifica:

- [ ] Ejecuté `python setup_complete.py` sin errores
- [ ] El script mostró "✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE"
- [ ] Detuve el servidor Flask (`Ctrl + C`)
- [ ] Inicié el servidor nuevamente (`python run.py`)
- [ ] El servidor está corriendo (veo "Running on http://127.0.0.1:5000")
- [ ] Abrí el navegador en modo incógnito
- [ ] Fui a http://localhost:5000
- [ ] Hice login como `terapeuta` / `tera123`
- [ ] Fui a "Galería de Videos"
- [ ] Intenté compartir un video
- [ ] Abrí DevTools (F12) para ver errores
- [ ] Verifiqué la pestaña "Network" → "get-patients-for-sharing"
- [ ] La respuesta muestra `"total": 5`

---

## 🎥 Captura de Pantalla de Referencia

**Así debería verse el selector:**

```
┌───────────────────────────────────────────────┐
│ 🎥 Compartir Video con Paciente               │
├───────────────────────────────────────────────┤
│                                               │
│ Seleccionar Paciente:                         │
│ ┌───────────────────────────────────────────┐ │
│ │ Andrea Luna - Rehabilitación rodilla      │ │
│ │ María García - Lesión de hombro           │ │
│ │ Juan Pérez - Rehabilitación de cadera     │ │
│ │ Carlos Rodríguez - Lesión lumbar          │ │
│ │ Sofía Martínez - Rehabilitación de tobillo│ │
│ └───────────────────────────────────────────┘ │
│                                               │
│ Mensaje (opcional):                           │
│ ┌───────────────────────────────────────────┐ │
│ │                                           │ │
│ │                                           │ │
│ └───────────────────────────────────────────┘ │
│                                               │
│ [Cancelar]  [📤 Compartir Video]              │
└───────────────────────────────────────────────┘
```

---

## 🆘 Última Opción

Si después de TODO esto aún no funciona:

1. **Cierra TODO:**
   - Cierra el navegador completamente
   - Detén el servidor (`Ctrl + C`)
   - Cierra la terminal

2. **Reinicia desde cero:**
   ```bash
   # Abrir nueva terminal
   cd web-RehabSystem
   
   # Configurar base de datos
   python setup_complete.py
   
   # Iniciar servidor
   python run.py
   ```

3. **Abrir navegador:**
   - Modo incógnito
   - http://localhost:5000
   - Login: terapeuta / tera123
   - Galería de Videos
   - Compartir video

4. **Si TODAVÍA no funciona:**
   - Toma captura de pantalla del selector vacío
   - Toma captura de DevTools → Console (errores)
   - Toma captura de DevTools → Network → get-patients-for-sharing (respuesta)
   - Copia la salida de: `python test_browser_simulation.py`

---

**Con estos pasos, DEBERÍA funcionar al 100%** ✅

---

**Última actualización:** 6 de diciembre de 2025
