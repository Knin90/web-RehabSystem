# 🐛 Instrucciones de Depuración - Ver Logs en el Navegador

**Objetivo:** Ver exactamente qué está devolviendo la API y por qué no aparecen los pacientes

---

## 📋 PASO 1: Asegúrate de que los datos están en la BD

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

✅ **Si ves esto, los datos están correctos**

---

## 📋 PASO 2: Reiniciar el Servidor

**IMPORTANTE:** El template fue modificado con logs de depuración.

```bash
# Detener servidor
Ctrl + C

# Iniciar nuevamente
python run.py
```

---

## 📋 PASO 3: Abrir Navegador con DevTools

1. **Abrir navegador en modo incógnito**
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`

2. **ANTES de ir a la página, abrir DevTools**
   - Presiona: `F12`
   - O Click derecho → "Inspeccionar"

3. **Ir a la pestaña "Console"**
   - Debe estar visible ANTES de cargar la página

---

## 📋 PASO 4: Login y Navegar

1. **Ir a:** http://localhost:5000

2. **Login:**
   - Usuario: `terapeuta`
   - Contraseña: `tera123`

3. **Ir a:** "Galería de Videos"

4. **Click en:** "Compartir con Paciente" (en cualquier video)

---

## 📋 PASO 5: Ver los Logs en la Consola

**En la consola de DevTools deberías ver:**

```
🔍 DEBUG: Llamando a /api/get-patients-for-sharing...
🔍 DEBUG: Response status: 200
🔍 DEBUG: Response headers: [object Headers]
🔍 DEBUG: Respuesta completa: {success: true, patients: Array(5), total: 5}
🔍 DEBUG: data.success: true
🔍 DEBUG: data.patients: (5) [{…}, {…}, {…}, {…}, {…}]
🔍 DEBUG: data.total: 5
🔍 DEBUG: Success = true
🔍 DEBUG: Número de pacientes: 5
✅ DEBUG: Generando opciones para 5 pacientes
  - Paciente: Andrea Luna (ID: 1)
  - Paciente: María García (ID: 2)
  - Paciente: Juan Pérez (ID: 3)
  - Paciente: Carlos Rodríguez (ID: 4)
  - Paciente: Sofía Martínez (ID: 5)
✅ DEBUG: Opciones agregadas al select
```

---

## 🎯 INTERPRETACIÓN DE LOS LOGS

### ✅ **CASO 1: Ves los 5 pacientes en los logs**

**Logs:**
```
✅ DEBUG: Generando opciones para 5 pacientes
  - Paciente: Andrea Luna (ID: 1)
  - Paciente: María García (ID: 2)
  ...
✅ DEBUG: Opciones agregadas al select
```

**Pero NO aparecen en el selector:**

**Problema:** Error de JavaScript o DOM

**Solución:**
1. Verifica que el elemento `sharePatientSelect` existe
2. En la consola, escribe:
   ```javascript
   document.getElementById('sharePatientSelect')
   ```
3. Debería mostrar el elemento `<select>`
4. Si muestra `null`, el modal no se abrió correctamente

---

### ⚠️ **CASO 2: Ves "No tienes pacientes asignados"**

**Logs:**
```
⚠️ DEBUG: No hay pacientes asignados
```

**Problema:** La API devuelve 0 pacientes

**Solución:**
```bash
# Ejecutar nuevamente
python setup_complete.py

# Reiniciar servidor
Ctrl + C
python run.py

# Probar nuevamente
```

---

### ❌ **CASO 3: Ves "Error de conexión"**

**Logs:**
```
❌ DEBUG: Error en fetch: ...
```

**Problema:** No se puede conectar a la API

**Solución:**
1. Verifica que el servidor está corriendo
2. Verifica la URL: http://localhost:5000
3. Verifica que estás logueado como terapeuta

---

### 🔴 **CASO 4: Response status: 302**

**Logs:**
```
🔍 DEBUG: Response status: 302
```

**Problema:** Redirect a login (no estás autenticado)

**Solución:**
1. Cierra el navegador completamente
2. Abre modo incógnito nuevamente
3. Login como terapeuta
4. Intenta nuevamente

---

### 🔴 **CASO 5: Response status: 500**

**Logs:**
```
🔍 DEBUG: Response status: 500
```

**Problema:** Error en el servidor

**Solución:**
1. Mira la terminal del servidor
2. Busca el error en rojo
3. Copia el error completo

---

## 📸 CAPTURA DE PANTALLA

**Por favor, toma captura de pantalla de:**

1. **La consola completa** (F12 → Console)
   - Debe mostrar todos los logs de DEBUG

2. **El selector** (el dropdown que está vacío)

3. **La pestaña Network** (F12 → Network)
   - Busca: `get-patients-for-sharing`
   - Click en ella
   - Ve a "Response"
   - Toma captura de la respuesta JSON

---

## 🔍 VERIFICACIÓN ADICIONAL

### En la Consola del Navegador, escribe:

```javascript
// Ver el elemento select
document.getElementById('sharePatientSelect')

// Ver las opciones del select
document.getElementById('sharePatientSelect').options

// Ver el HTML del select
document.getElementById('sharePatientSelect').innerHTML
```

**Copia y pega los resultados**

---

## 📋 CHECKLIST ANTES DE REPORTAR

- [ ] Ejecuté `python test_browser_simulation.py` → Muestra 5 pacientes
- [ ] Ejecuté `python setup_complete.py` → Sin errores
- [ ] Reinicié el servidor (`Ctrl + C` → `python run.py`)
- [ ] Abrí navegador en modo incógnito
- [ ] Abrí DevTools (F12) ANTES de cargar la página
- [ ] Fui a la pestaña "Console"
- [ ] Hice login como `terapeuta` / `tera123`
- [ ] Fui a "Galería de Videos"
- [ ] Intenté compartir un video
- [ ] Vi los logs en la consola
- [ ] Tomé captura de pantalla de la consola
- [ ] Tomé captura de pantalla del selector
- [ ] Tomé captura de pantalla de Network → Response

---

## 📤 QUÉ ENVIAR

Si después de todo esto aún no funciona, envía:

1. **Captura de pantalla de la consola** (con los logs de DEBUG)
2. **Captura de pantalla del selector vacío**
3. **Captura de pantalla de Network → get-patients-for-sharing → Response**
4. **Salida de:** `python test_browser_simulation.py`
5. **Resultado de ejecutar en la consola:**
   ```javascript
   document.getElementById('sharePatientSelect').innerHTML
   ```

Con esta información podré identificar exactamente dónde está el problema.

---

**Última actualización:** 6 de diciembre de 2025
