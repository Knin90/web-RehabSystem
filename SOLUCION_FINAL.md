# 🎯 SOLUCIÓN FINAL - Pacientes No Aparecen en Selector

**Problema:** Al intentar compartir un video, el selector muestra "No tienes pacientes asignados"  
**Causa:** La base de datos no tiene pacientes asignados al terapeuta  
**Solución:** Ejecutar el script de configuración completa

---

## ✅ SOLUCIÓN RÁPIDA (3 pasos)

### Paso 1: Ejecutar Script de Configuración

```bash
python setup_complete.py
```

**Este script hace TODO automáticamente:**
- ✅ Limpia la base de datos
- ✅ Crea usuarios (admin, terapeuta, 5 pacientes)
- ✅ Crea 8 ejercicios
- ✅ Asigna los 5 pacientes al terapeuta
- ✅ Crea rutinas para cada paciente

**Salida esperada:**
```
✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE
============================================================

📊 RESUMEN:
  - Usuarios: 7
  - Terapeutas: 1
  - Pacientes: 5
  - Ejercicios: 8
  - Rutinas: 5

👥 Pacientes asignados a Rafael Lu: 5
  - Andrea Luna
  - María García
  - Juan Pérez
  - Carlos Rodríguez
  - Sofía Martínez
```

### Paso 2: Reiniciar el Servidor

**Si el servidor está corriendo:**
1. Presiona `Ctrl + C` para detenerlo
2. Ejecuta nuevamente:

```bash
python run.py
```

**Salida esperada:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### Paso 3: Probar en el Navegador

1. **Abrir navegador en modo incógnito** (para evitar caché)
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`
   - Edge: `Ctrl + Shift + N`

2. **Ir a:** http://localhost:5000

3. **Login como terapeuta:**
   - Usuario: `terapeuta`
   - Contraseña: `tera123`

4. **Ir a "Galería de Videos"**

5. **Click en "Compartir con Paciente"**

6. **✅ AHORA DEBERÍAS VER:**
   ```
   Seleccionar Paciente:
   ├── Andrea Luna - Rehabilitación rodilla
   ├── María García - Lesión de hombro
   ├── Juan Pérez - Rehabilitación de cadera
   ├── Carlos Rodríguez - Lesión lumbar
   └── Sofía Martínez - Rehabilitación de tobillo
   ```

---

## 🔍 Verificación Antes de Probar

Si quieres verificar que todo está bien antes de reiniciar el servidor:

```bash
python debug_api_patients.py
```

**Deberías ver:**
```
✓ Pacientes obtenidos: 5

📋 LISTA DE PACIENTES ASIGNADOS:
1. Andrea Luna
2. María García
3. Juan Pérez
4. Carlos Rodríguez
5. Sofía Martínez
```

---

## 📝 Credenciales del Sistema

### Terapeuta (para compartir videos)
- **Usuario:** `terapeuta`
- **Contraseña:** `tera123`
- **Nombre:** Rafael Lu
- **Pacientes asignados:** 5

### Pacientes (para recibir videos)

| Nombre | Usuario | Contraseña |
|--------|---------|-----------|
| Andrea Luna | `paciente` | `paci123` |
| María García | `maria_garcia` | `maria123` |
| Juan Pérez | `juan_perez` | `juan123` |
| Carlos Rodríguez | `carlos_rodriguez` | `carlos123` |
| Sofía Martínez | `sofia_martinez` | `sofia123` |

### Admin
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 🐛 Si Aún No Funciona

### Opción 1: Verificar la API Directamente

1. **Asegúrate de estar logueado como terapeuta**
2. **Abre la consola del navegador** (F12)
3. **Ve a la pestaña "Network"**
4. **Intenta compartir un video**
5. **Busca la petición:** `get-patients-for-sharing`
6. **Click en ella y ve la respuesta**

**Respuesta correcta:**
```json
{
  "success": true,
  "patients": [
    {"id": 1, "name": "Andrea Luna", ...},
    {"id": 2, "name": "María García", ...},
    ...
  ],
  "total": 5
}
```

**Respuesta incorrecta:**
```json
{
  "success": true,
  "patients": [],
  "total": 0
}
```

Si ves `"total": 0`, ejecuta nuevamente `setup_complete.py`

### Opción 2: Verificar Errores en la Consola

1. **Abre DevTools** (F12)
2. **Ve a la pestaña "Console"**
3. **Busca errores en rojo**
4. **Copia el error y búscalo en el código**

### Opción 3: Verificar que el Servidor Está Actualizado

1. **Detén el servidor** (`Ctrl + C`)
2. **Verifica que no hay otro servidor corriendo:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Si hay algo, mata el proceso
   taskkill /PID <numero_pid> /F
   ```
3. **Inicia el servidor nuevamente:**
   ```bash
   python run.py
   ```

---

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────┐
│ 1. Ejecutar setup_complete.py      │
│    ✓ Crea 5 pacientes               │
│    ✓ Asigna al terapeuta            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Reiniciar servidor Flask         │
│    Ctrl+C → python run.py           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Abrir navegador (incógnito)     │
│    http://localhost:5000            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Login como terapeuta             │
│    terapeuta / tera123              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Galería de Videos                │
│    → Compartir con Paciente         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ ✅ Ver 5 pacientes en el selector   │
└─────────────────────────────────────┘
```

---

## 🎯 Casos de Prueba

### Caso 1: Terapeuta Comparte con Andrea Luna
1. Login: `terapeuta` / `tera123`
2. Galería de Videos → Compartir con Paciente
3. Seleccionar: **Andrea Luna - Rehabilitación rodilla**
4. Mensaje: "Revisa tu postura"
5. Compartir
6. ✅ Éxito

### Caso 2: Andrea Luna Ve el Video
1. Logout del terapeuta
2. Login: `paciente` / `paci123`
3. Galería de Videos → Pestaña "Videos Compartidos"
4. ✅ Ver video del terapeuta con mensaje

### Caso 3: María García Comparte con Terapeuta
1. Login: `maria_garcia` / `maria123`
2. Galería de Videos → Mis Videos
3. Compartir con Terapeuta → Seleccionar: **Rafael Lu**
4. Mensaje: "¿Estoy haciendo bien el ejercicio?"
5. Compartir
6. ✅ Éxito

---

## 🆘 Contacto de Soporte

Si después de seguir todos estos pasos aún no funciona, proporciona:

1. **Salida de:**
   ```bash
   python debug_api_patients.py
   ```

2. **Captura de pantalla del selector vacío**

3. **Errores en la consola del navegador** (F12 → Console)

4. **Respuesta de la API** (F12 → Network → get-patients-for-sharing)

---

## ✅ Checklist Final

Antes de reportar un problema, verifica:

- [ ] Ejecuté `python setup_complete.py` sin errores
- [ ] `debug_api_patients.py` muestra 5 pacientes
- [ ] Reinicié el servidor Flask
- [ ] Abrí el navegador en modo incógnito
- [ ] Estoy logueado como `terapeuta` / `tera123`
- [ ] Fui a "Galería de Videos"
- [ ] Intenté compartir un video
- [ ] La consola del navegador no muestra errores

---

**Si todos los checks están ✅ y aún no funciona, hay un problema más profundo que necesita investigación adicional.**

---

**Última actualización:** 6 de diciembre de 2025  
**Versión:** 1.0 - Solución Final
