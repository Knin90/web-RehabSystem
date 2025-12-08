# 🔴 SOLUCIÓN: Error de Conexión a Base de Datos

## ❌ Problema Actual

Tu aplicación está corriendo pero falla al intentar login con este error:

```
could not translate host name "dpg-xxxxx" to address
```

**Causa**: DATABASE_URL tiene un placeholder `dpg-xxxxx` en lugar de la URL real de PostgreSQL.

## ✅ Solución en 3 Pasos

### Paso 1: Verificar si Existe la Base de Datos PostgreSQL

1. Ve a tu **Render Dashboard**: https://dashboard.render.com
2. Busca en la lista de servicios si existe **"rehab-db"** o alguna base de datos PostgreSQL
3. **¿La encontraste?**
   - ✅ **SÍ** → Salta al **Paso 2**
   - ❌ **NO** → Continúa con **Paso 1.1**

#### Paso 1.1: Crear Base de Datos PostgreSQL (si no existe)

1. En Render Dashboard, click en **"New +"** (arriba a la derecha)
2. Selecciona **"PostgreSQL"**
3. Configura:
   ```
   Name: rehab-db
   Database: rehab_system
   User: rehab_user
   Region: Oregon (US West) - o la más cercana
   Plan: Free
   ```
4. Click **"Create Database"**
5. **Espera 2-3 minutos** hasta que el status sea "Available"

### Paso 2: Conectar DATABASE_URL Correctamente

**⚠️ IMPORTANTE**: NO escribas la URL manualmente. Usa el ícono de enlace.

1. Ve a tu **Web Service** (web-rehabsystem-1)
2. Click en **"Environment"** (menú lateral izquierdo)
3. Busca la variable **DATABASE_URL**
4. Si existe:
   - Click en el **ícono de lápiz** (editar)
   - Borra el valor actual
5. Si no existe:
   - Click **"Add Environment Variable"**
   - Key: `DATABASE_URL`
6. **CRUCIAL**: Click en el **ícono de enlace** 🔗 (al lado del campo Value)
7. En el popup:
   - Selecciona: **rehab-db** (tu base de datos)
   - Property: **Internal Database URL**
8. Click **"Save Changes"**

### Paso 3: Esperar Redeploy y Verificar

1. Render hará **redeploy automático** (5-10 minutos)
2. Ve a la pestaña **"Logs"**
3. Espera a ver estos mensajes:
   ```
   ==> Building...
   ==> Deploying...
   ==> Starting service...
   Inicializando base de datos...
   ✓ Tablas creadas/verificadas
   ✓ Datos iniciales creados
   Starting gunicorn...
   Listening at: http://0.0.0.0:10000
   ```
4. Abre tu aplicación: https://web-rehabsystem-1.onrender.com
5. Prueba login:
   - Usuario: `admin`
   - Contraseña: `admin123`

## 🎯 ¿Por Qué Falló?

DATABASE_URL tenía un valor como:
```
postgresql://user:pass@dpg-xxxxx/database
```

El `dpg-xxxxx` es un **placeholder**, no una dirección real. Render necesita que uses el ícono de enlace 🔗 para conectar automáticamente la URL correcta de tu base de datos.

## 🔍 Verificar que Está Bien Configurado

Después de conectar DATABASE_URL con el ícono de enlace, deberías ver algo como:

```
DATABASE_URL = postgresql://rehab_user:abc123xyz@dpg-ct9abc123xyz-a.oregon-postgres.render.com/rehab_system
```

**Nota**: La URL real tendrá un host completo como `dpg-ct9abc123xyz-a.oregon-postgres.render.com`, NO solo `dpg-xxxxx`.

## 📊 Checklist Rápido

```
□ Base de datos PostgreSQL creada (rehab-db)
□ DATABASE_URL conectada con ícono de enlace 🔗
□ Redeploy completado sin errores
□ Logs muestran "Inicializando base de datos..."
□ Logs muestran "✓ Datos iniciales creados"
□ Aplicación abre sin error 500
□ Login funciona con admin/admin123
```

## 🚨 Si Aún Falla

### Error: "No module named 'psycopg2'"
**Solución**: Ya está en requirements.txt, solo espera el redeploy completo.

### Error: "Application failed to start"
**Solución**: Verifica que SECRET_KEY también esté configurada:
```bash
# Genera una:
python -c "import secrets; print(secrets.token_hex(32))"

# Agrégala en Environment:
Key: SECRET_KEY
Value: <pegar-clave-generada>
```

### Error: "Internal Server Error" después de login
**Solución**: La base de datos no se inicializó. Verifica en logs que aparezca "✓ Datos iniciales creados".

## 🎉 Resultado Esperado

Después de estos pasos:
- ✅ Aplicación carga sin errores
- ✅ Página de login se muestra
- ✅ Login con admin/admin123 funciona
- ✅ Dashboard se muestra correctamente
- ✅ Base de datos tiene usuarios y datos iniciales

## 📞 Próximo Paso

**AHORA MISMO**:
1. Ve a Render Dashboard
2. Verifica/crea base de datos PostgreSQL
3. Conecta DATABASE_URL con ícono de enlace 🔗
4. Espera redeploy (5-10 min)
5. Prueba login

---

**Tiempo estimado**: 10-15 minutos total
