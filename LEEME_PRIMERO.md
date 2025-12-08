# 🚨 LEE ESTO PRIMERO - SOLUCIÓN RÁPIDA

## ❌ PROBLEMA
No se muestran los nombres de los pacientes cuando el terapeuta intenta compartir un video.

## ✅ SOLUCIÓN RÁPIDA (3 MINUTOS)

### OPCIÓN 1: Usar el script automático (Windows)

Haz doble click en:
```
ARREGLAR_PACIENTES.bat
```

Sigue las instrucciones en pantalla.

---

### OPCIÓN 2: Comandos manuales

Abre una terminal en la carpeta `web-RehabSystem` y ejecuta:

```bash
# 1. Configurar base de datos con pacientes
python setup_complete.py

# 2. Verificar que funcionó
python verificar_pacientes.py

# 3. Reiniciar servidor (si está corriendo, presiona Ctrl+C primero)
python run.py
```

Luego en el navegador:
1. Abre en modo incógnito (`Ctrl + Shift + N`)
2. Ve a: `http://localhost:5000/login`
3. Login: `terapeuta` / `tera123`
4. Click en "Galería de Videos"
5. Click en "Compartir con Paciente" en cualquier video
6. **Deberías ver 5 pacientes en el selector**

---

## 📚 DOCUMENTACIÓN COMPLETA

Si la solución rápida no funciona, lee:

- **SOLUCION_COMPARTIR_PACIENTES.md** - Guía paso a paso detallada
- **DIAGNOSTICO_FINAL.md** - Diagnóstico técnico del problema
- **INSTRUCCIONES_DEBUG.md** - Cómo usar DevTools para debugging

---

## 🧪 SCRIPTS DE VERIFICACIÓN

- `setup_complete.py` - Crea la base de datos con 5 pacientes
- `verificar_pacientes.py` - Verifica que los pacientes estén asignados
- `test_browser_simulation.py` - Simula lo que hace el navegador

---

## 🎯 ¿QUÉ HACE setup_complete.py?

Este script:
1. ✅ Limpia la base de datos
2. ✅ Crea usuario admin
3. ✅ Crea terapeuta "Rafael Lu"
4. ✅ Crea 5 pacientes:
   - Andrea Luna
   - María García
   - Juan Pérez
   - Carlos Rodríguez
   - Sofía Martínez
5. ✅ Crea rutinas que asignan cada paciente al terapeuta
6. ✅ Crea ejercicios de ejemplo

**Después de ejecutarlo, el terapeuta tendrá 5 pacientes asignados.**

---

## 🔍 ¿CÓMO VERIFICO QUE FUNCIONÓ?

### En la Terminal:

Ejecuta:
```bash
python verificar_pacientes.py
```

Debes ver:
```
✅ VERIFICACIÓN EXITOSA
👥 LISTA DE PACIENTES ASIGNADOS:
   1. Andrea Luna
   2. María García
   3. Juan Pérez
   4. Carlos Rodríguez
   5. Sofía Martínez
```

### En el Navegador:

1. Abre DevTools (`F12`)
2. Ve a la pestaña **Console**
3. Intenta compartir un video
4. Debes ver:
```
✅ DEBUG: Generando opciones para 5 pacientes
  - Paciente: Andrea Luna (ID: 1)
  - Paciente: María García (ID: 2)
  - Paciente: Juan Pérez (ID: 3)
  - Paciente: Carlos Rodríguez (ID: 4)
  - Paciente: Sofía Martínez (ID: 5)
```

---

## ⚠️ IMPORTANTE

### Antes de ejecutar setup_complete.py:

**Este script BORRA TODA LA BASE DE DATOS y la recrea desde cero.**

Si tienes datos importantes, haz un backup primero.

### Credenciales después de ejecutar el script:

```
Admin:
  Usuario: admin
  Contraseña: admin123

Terapeuta:
  Usuario: terapeuta
  Contraseña: tera123

Pacientes:
  Andrea Luna: paciente / paci123
  María García: maria_garcia / maria123
  Juan Pérez: juan_perez / juan123
  Carlos Rodríguez: carlos_rodriguez / carlos123
  Sofía Martínez: sofia_martinez / sofia123
```

---

## 🚀 RESUMEN ULTRA RÁPIDO

```bash
python setup_complete.py
python run.py
```

Luego en el navegador (modo incógnito):
- Login: `terapeuta` / `tera123`
- Galería de Videos → Compartir con Paciente
- **Ver 5 pacientes en el selector**

---

## 📞 SI NADA FUNCIONA

1. Ejecuta: `python test_browser_simulation.py`
2. Captura la salida
3. Abre DevTools (F12) en el navegador
4. Captura la consola cuando intentas compartir
5. Proporciona ambas capturas

---

## ✅ CHECKLIST

- [ ] Ejecuté `python setup_complete.py`
- [ ] Vi el mensaje "✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE"
- [ ] Ejecuté `python verificar_pacientes.py`
- [ ] Vi "Pacientes asignados: 5"
- [ ] Reinicié el servidor Flask
- [ ] Abrí navegador en modo incógnito
- [ ] Hice login como terapeuta
- [ ] Abrí DevTools (F12)
- [ ] Intenté compartir un video
- [ ] Vi los logs en la consola

Si completaste todos estos pasos y aún no funciona, hay un problema más profundo que necesita investigación adicional.
