# 📸 Instrucciones Visuales - Basado en tu Pantalla

## 🔍 Lo que Veo en tu Imagen

Tu pantalla de Environment muestra:

| KEY | VALUE |
|-----|-------|
| DATABASE_URL | `postgresql://rehab_user:password@dpg-xxxxx/rehab_system` |
| FLASK_APP | `run.py` |
| FLASK_ENV | `production` |
| SECRET_KEY | `c74bc098c062d46bbccbb4e1af8fc7a1` |

**Problema identificado**: `dpg-xxxxx` no es una dirección real.

---

## ✅ Solución Paso a Paso (Con Capturas Mentales)

### 🎯 Paso 1: Editar DATABASE_URL

**En la pantalla que estás viendo ahora:**

1. Busca la fila de **DATABASE_URL** (primera fila)
2. Al final de esa fila, verás un **ícono de lápiz** ✏️
3. **Click en el ícono de lápiz**

**Se abrirá un formulario de edición:**

```
Key: DATABASE_URL
Value: [campo de texto con la URL actual]
[🔗] ← Ícono de enlace aquí
```

---

### 🎯 Paso 2: Usar el Ícono de Enlace

**En el formulario de edición:**

1. **Borra el contenido** del campo Value (el que tiene `dpg-xxxxx`)
2. Busca el **ícono de enlace** 🔗 (está al lado derecho del campo Value)
3. **Click en el ícono de enlace** 🔗

**Se abrirá un popup:**

```
┌─────────────────────────────────┐
│ Link to Database                │
├─────────────────────────────────┤
│ Service: [Dropdown ▼]           │
│ Property: [Dropdown ▼]          │
│                                 │
│ [Cancel]  [Link]                │
└─────────────────────────────────┘
```

4. En **"Service"**: Selecciona tu base de datos (probablemente `rehab-db`)
   - Si no aparece ninguna base de datos, necesitas crearla primero (ver Paso 2A)
5. En **"Property"**: Selecciona `Internal Database URL`
6. Click **"Link"**

**El campo Value se llenará automáticamente con algo como:**
```
postgresql://rehab_user:abc123xyz@dpg-ct9abc123xyz-a.oregon-postgres.render.com/rehab_system
```

7. **Click "Save"** o **"Update"**

---

### 🎯 Paso 2A: Si No Tienes Base de Datos (Crear una)

**Si en el dropdown de "Service" no aparece ninguna base de datos:**

1. **Cancela** el popup
2. **Abre una nueva pestaña** en tu navegador
3. Ve a: https://dashboard.render.com
4. Click en **"New +"** (botón azul arriba a la derecha)
5. Selecciona **"PostgreSQL"**

**Formulario de creación:**

```
Name: rehab-db
Database: rehab_system
User: rehab_user
Region: Oregon (US West)
PostgreSQL Version: 16
Plan: Free
```

6. Click **"Create Database"**
7. **Espera 2-3 minutos** hasta que el status sea "Available"
8. **Vuelve a la pestaña** de tu Web Service
9. **Repite el Paso 2** (usar ícono de enlace)

---

### 🎯 Paso 3: Guardar Cambios

**Después de actualizar DATABASE_URL:**

1. Scroll hasta el final de la página de Environment
2. Verás un botón **"Save Changes"**
3. **Click en "Save Changes"**

**Render mostrará:**
```
✓ Environment variables updated
Deploying...
```

---

### 🎯 Paso 4: Actualizar Start Command

**En el menú lateral izquierdo:**

1. Click en **"Settings"**
2. Scroll hasta la sección **"Build & Deploy"**
3. Busca **"Start Command"**

**Verás algo como:**
```
Start Command: gunicorn run:app --bind 0.0.0.0:$PORT
[Edit]
```

4. Click en **"Edit"** o en el campo
5. **Borra el contenido actual**
6. **Escribe**: `bash start.sh`
7. Click **"Save Changes"**

---

### 🎯 Paso 5: Monitorear el Deploy

**En el menú lateral izquierdo:**

1. Click en **"Logs"**
2. Verás el proceso de deploy en tiempo real
3. **Espera 5-10 minutos**

**Busca estos mensajes:**

```
==> Building...
==> Installing dependencies...
Successfully installed Flask-3.1.2 ...
==> Build successful

==> Deploying...
==> Starting service...

Importando módulos...
Creando aplicación...
Inicializando contexto...
Creando tablas...
✓ Tablas creadas/verificadas
✓ Datos iniciales creados
  - Admin: admin / admin123

Starting gunicorn 21.2.0
Listening at: http://0.0.0.0:10000
```

**Si ves "Listening at: http://0.0.0.0:10000" → ¡Éxito! ✅**

---

### 🎯 Paso 6: Probar la Aplicación

1. En el menú superior, verás la **URL de tu aplicación**
2. Click en la URL o cópiala
3. Ábrela en una nueva pestaña
4. Deberías ver la **página de login**
5. Ingresa:
   - Usuario: `admin`
   - Contraseña: `admin123`
6. Click **"Iniciar Sesión"**

**Si ves el Dashboard → ¡TODO FUNCIONA! 🎉**

---

## 🚨 Qué Hacer Si Algo Sale Mal

### Error en Logs: "could not translate host name"
**Significa**: DATABASE_URL todavía tiene `dpg-xxxxx`
**Solución**: Repite el Paso 2, asegúrate de usar el ícono de enlace 🔗

### Error en Logs: "No module named 'psycopg2'"
**Significa**: Build incompleto
**Solución**: Espera a que termine el build completo (puede tomar 10 min)

### Error en Logs: "password authentication failed"
**Significa**: La contraseña en DATABASE_URL es incorrecta
**Solución**: Usa el ícono de enlace 🔗 en lugar de copiar manualmente

### No veo "✓ Datos iniciales creados"
**Significa**: Start Command no está actualizado
**Solución**: Verifica que Start Command sea exactamente `bash start.sh`

### Error 500 al abrir la aplicación
**Significa**: La base de datos no se inicializó
**Solución**: Revisa los logs, debe aparecer "✓ Datos iniciales creados"

---

## 📋 Checklist Visual

Marca cada paso cuando lo completes:

```
□ Paso 1: Click en ícono de lápiz ✏️ en DATABASE_URL
□ Paso 2: Click en ícono de enlace 🔗
□ Paso 2: Seleccionar rehab-db en Service
□ Paso 2: Seleccionar Internal Database URL en Property
□ Paso 2: Click en Link
□ Paso 3: Click en Save Changes
□ Paso 4: Ir a Settings
□ Paso 4: Cambiar Start Command a "bash start.sh"
□ Paso 4: Click en Save Changes
□ Paso 5: Ir a Logs
□ Paso 5: Esperar "Listening at: http://0.0.0.0:10000"
□ Paso 6: Abrir URL de la aplicación
□ Paso 6: Login con admin/admin123
□ Paso 6: Ver Dashboard
```

---

## 🎯 Resumen Ultra-Rápido

Desde la pantalla que estás viendo ahora:

1. **DATABASE_URL** → ✏️ → 🔗 → rehab-db → Internal Database URL → Save
2. **Settings** → Start Command → `bash start.sh` → Save
3. **Logs** → Esperar "Listening at..."
4. **Abrir URL** → Login admin/admin123

**Tiempo**: 10-15 minutos

---

## 💡 Tip Importante

**El ícono de enlace 🔗 es tu mejor amigo** porque:
- Conecta automáticamente la URL correcta
- No hay errores de tipeo
- Render maneja todo por ti

**NO intentes escribir la URL manualmente** a menos que sea absolutamente necesario.

---

**¿Listo para empezar?** Sigue el Paso 1 ⬆️
