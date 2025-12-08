# 🚨 SOLUCIÓN RÁPIDA - Error de Base de Datos

## El Problema

Tu app está corriendo pero falla al hacer login con:
```
could not translate host name "dpg-xxxxx" to address
```

## La Solución (3 pasos - 10 minutos)

### Paso 1: Crear Base de Datos (si no existe)

1. Ve a https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configura:
   - Name: `rehab-db`
   - Database: `rehab_system`
   - User: `rehab_user`
   - Plan: Free
4. Click **"Create Database"**
5. Espera 2-3 minutos

### Paso 2: Conectar DATABASE_URL

1. Ve a tu **Web Service** (web-rehabsystem-1)
2. Click **"Environment"**
3. Busca **DATABASE_URL**
4. Click **ícono de lápiz** (editar)
5. **Click en ícono de enlace** 🔗 (NO escribas manualmente)
6. Selecciona: **rehab-db** → **Internal Database URL**
7. Click **"Save Changes"**

### Paso 3: Actualizar Start Command

1. Click **"Settings"**
2. Busca **"Start Command"**
3. Cambia a: `bash start.sh`
4. Click **"Save Changes"**

## Esperar y Verificar

1. Render hará redeploy automático (5-10 min)
2. Ve a **"Logs"** y espera ver:
   ```
   ✓ Datos iniciales creados
   Starting gunicorn...
   Listening at: http://0.0.0.0:10000
   ```
3. Abre: https://web-rehabsystem-1.onrender.com
4. Login: `admin` / `admin123`

## ¿Necesitas Más Detalles?

Lee: `docs/ARREGLAR_DATABASE_URL.md`

---

**Tiempo total**: 10-15 minutos
