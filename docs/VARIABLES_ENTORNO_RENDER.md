# Variables de Entorno para Render

## 📋 Variables Requeridas

### 1. FLASK_APP
```
Key: FLASK_APP
Value: run.py
```
**Estado**: ✅ Ya configurada

### 2. FLASK_ENV
```
Key: FLASK_ENV
Value: production
```
**Estado**: ✅ Ya configurada

### 3. SECRET_KEY
```
Key: SECRET_KEY
Value: <generar-clave-segura>
```

**Cómo generar**:
```python
import secrets
print(secrets.token_hex(32))
# Ejemplo: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

**Estado**: ⚠️ FALTA AGREGAR

### 4. DATABASE_URL
```
Key: DATABASE_URL
Value: <conectar-desde-base-de-datos>
```

**Cómo configurar**:
1. Click en **"Add Environment Variable"**
2. Key: `DATABASE_URL`
3. Click en el ícono de **enlace** (🔗)
4. Selecciona tu base de datos: `rehab-db`
5. Property: **Internal Database URL**

**Estado**: ⚠️ FALTA CONECTAR

## 🔧 Pasos para Completar Configuración

### Paso 1: Generar SECRET_KEY

Opción A - Python local:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Opción B - Online:
```
https://randomkeygen.com/
Usar: Fort Knox Passwords (256-bit)
```

### Paso 2: Agregar SECRET_KEY en Render

1. En tu Web Service, ve a **"Environment"**
2. Click **"Add Environment Variable"**
3. Key: `SECRET_KEY`
4. Value: `<pegar-clave-generada>`
5. Click **"Save Changes"**

### Paso 3: Conectar DATABASE_URL

**IMPORTANTE**: Primero debes crear la base de datos PostgreSQL

#### 3.1 Crear Base de Datos (si no existe)

1. En Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configurar:
   ```
   Name: rehab-db
   Database: rehab_system
   User: rehab_user
   Region: Oregon (US West) - misma región que tu web service
   Plan: Free (para desarrollo)
   ```
3. Click **"Create Database"**
4. Esperar 2-3 minutos a que se cree

#### 3.2 Conectar DATABASE_URL

1. Volver a tu Web Service
2. Ve a **"Environment"**
3. Click **"Add Environment Variable"**
4. Key: `DATABASE_URL`
5. **NO escribas el valor manualmente**
6. Click en el ícono de **enlace** (🔗) a la derecha
7. Selecciona: `rehab-db`
8. Property: **Internal Database URL**
9. Click **"Save Changes"**

## ✅ Verificación Final

Después de agregar todas las variables, deberías tener:

```
FLASK_APP = run.py
FLASK_ENV = production
SECRET_KEY = a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6... (64 caracteres)
DATABASE_URL = postgresql://rehab_user:password@dpg-xxxxx/rehab_system
```

## 🚀 Deploy

Después de configurar las variables:

1. Render automáticamente hará **redeploy**
2. Espera 5-10 minutos
3. Verifica en **"Logs"** que no haya errores

## 🔍 Verificar Configuración

### Ver Logs:
1. En tu Web Service, click **"Logs"**
2. Busca líneas como:
   ```
   Starting gunicorn...
   Booting worker with pid: xxx
   ```

### Probar Aplicación:
1. Abre la URL: `https://web-rehabsystem-1.onrender.com`
2. Deberías ver la página de login
3. Si ves error 500, revisa los logs

## 🐛 Solución de Problemas

### Error: "SECRET_KEY not set"
```bash
# Agregar SECRET_KEY en Environment
# Generar con: python -c "import secrets; print(secrets.token_hex(32))"
```

### Error: "Could not connect to database"
```bash
# Verificar que DATABASE_URL está conectada
# Debe ser Internal Database URL, no External
# Verificar que la base de datos está en estado "Available"
```

### Error: "Application failed to start"
```bash
# Verificar requirements.txt incluye:
gunicorn==21.2.0
psycopg2-binary==2.9.9

# Verificar Start Command:
gunicorn run:app --bind 0.0.0.0:$PORT
```

## 📝 Configuración Completa Ejemplo

```bash
# Variables de Entorno en Render
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
DATABASE_URL=postgresql://rehab_user:abc123@dpg-xxxxx-a/rehab_system

# Build Command
pip install -r requirements.txt

# Start Command
gunicorn run:app --bind 0.0.0.0:$PORT
```

## 🎯 Próximos Pasos

Después de configurar las variables:

1. ✅ Esperar a que termine el deploy
2. ✅ Abrir la aplicación
3. ✅ Inicializar base de datos:
   ```bash
   # Desde Render Shell
   python scripts/setup/setup_complete.py
   ```
4. ✅ Probar login con:
   - Usuario: `admin`
   - Contraseña: `admin123`

## 📚 Recursos

- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Render PostgreSQL](https://render.com/docs/databases)
- Documentación completa: `docs/CONFIGURACION_RENDER.md`
