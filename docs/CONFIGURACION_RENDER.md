# Guía de Configuración Manual en Render

Esta guía te ayudará a configurar manualmente el proyecto RehabSystem en Render.

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Repositorio en GitHub con el código
- Base de datos PostgreSQL (se creará en Render)

## 🗄️ Paso 1: Crear Base de Datos PostgreSQL

### 1.1 Desde el Dashboard de Render

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Click en **"New +"** → **"PostgreSQL"**
3. Configura la base de datos:

```
Name: rehab-db
Database: rehab_system
User: rehab_user
Region: Oregon (US West) o tu región preferida
PostgreSQL Version: 15 (recomendado)
Plan: Free (para desarrollo) o Starter (para producción)
```

4. Click en **"Create Database"**
5. **IMPORTANTE**: Guarda la información de conexión:
   - **Internal Database URL**: Para conexión desde Render
   - **External Database URL**: Para conexión externa
   - **PSQL Command**: Para conectar vía terminal

### 1.2 Información de Conexión

Después de crear la BD, verás algo como:

```
Internal Database URL:
postgresql://rehab_user:password@dpg-xxxxx-a/rehab_system

External Database URL:
postgresql://rehab_user:password@dpg-xxxxx-a.oregon-postgres.render.com/rehab_system

PSQL Command:
PGPASSWORD=password psql -h dpg-xxxxx-a.oregon-postgres.render.com -U rehab_user rehab_system
```

## 🚀 Paso 2: Crear Web Service

### 2.1 Configuración Básica

1. En el Dashboard, click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Selecciona el repositorio: `web-RehabSystem`
4. Configura el servicio:

```
Name: web-rehabsystem-1
Region: Oregon (US West) - misma región que la BD
Branch: main
Root Directory: . (punto, significa raíz)
Runtime: Python 3
```

### 2.2 Build & Deploy Settings

```
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn run:app --bind 0.0.0.0:$PORT
```

**Nota**: Render automáticamente asigna el puerto mediante la variable `$PORT`

### 2.3 Plan

```
Instance Type: Free (para desarrollo)
```

Para producción, considera:
- **Starter**: $7/mes - 512 MB RAM
- **Standard**: $25/mes - 2 GB RAM

## 🔐 Paso 3: Configurar Variables de Entorno

En la sección **"Environment"** del Web Service, agrega estas variables:

### Variables Requeridas:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=production

# Secret Key (generar una clave segura)
SECRET_KEY=tu_clave_super_secreta_aqui_cambiar

# Database URL (copiar de la BD creada en Paso 1)
DATABASE_URL=postgresql://rehab_user:password@dpg-xxxxx-a/rehab_system

# Puerto (Render lo asigna automáticamente)
PORT=10000
```

### Cómo Generar SECRET_KEY Segura:

Opción 1 - Python:
```python
import secrets
print(secrets.token_hex(32))
```

Opción 2 - Online:
```
https://randomkeygen.com/
```

### 3.1 Agregar Variables en Render

1. Ve a tu Web Service
2. Click en **"Environment"** en el menú lateral
3. Click en **"Add Environment Variable"**
4. Agrega cada variable:
   - Key: `FLASK_APP`
   - Value: `run.py`
5. Repite para todas las variables

### 3.2 Conectar Base de Datos

Para `DATABASE_URL`:
1. Click en **"Add Environment Variable"**
2. Key: `DATABASE_URL`
3. En lugar de escribir el valor, click en el ícono de enlace
4. Selecciona tu base de datos: `rehab-db`
5. Property: `Internal Database URL`

Esto conectará automáticamente tu web service con la base de datos.

## 📦 Paso 4: Archivos de Configuración

### 4.1 Verificar requirements.txt

Asegúrate de que `requirements.txt` incluya:

```txt
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-Migrate==4.0.5
python-dotenv==1.2.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

**IMPORTANTE**: `gunicorn` y `psycopg2-binary` son necesarios para producción.

### 4.2 Verificar Procfile (Opcional)

Si usas Procfile en lugar de Start Command:

```
web: gunicorn run:app --bind 0.0.0.0:$PORT
```

### 4.3 Actualizar app/config.py

Asegúrate de que `config.py` use variables de entorno:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///rehab.db'
    
    # Fix para PostgreSQL en Render
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max
```

## 🗃️ Paso 5: Inicializar Base de Datos

### 5.1 Conectar a la Base de Datos

Opción 1 - Desde Render Shell:
1. Ve a tu Web Service en Render
2. Click en **"Shell"** en el menú superior
3. Ejecuta los comandos SQL

Opción 2 - Desde tu computadora:
```bash
# Usar el PSQL Command de Render
PGPASSWORD=tu_password psql -h dpg-xxxxx-a.oregon-postgres.render.com -U rehab_user rehab_system
```

### 5.2 Ejecutar Script SQL

Ver archivo `scripts/sql/schema.sql` para el esquema completo.

Desde el shell de Render:
```bash
# Opción 1: Ejecutar script Python
python scripts/setup/setup_complete.py

# Opción 2: Ejecutar SQL directamente
psql $DATABASE_URL < scripts/sql/schema.sql
psql $DATABASE_URL < scripts/sql/seed_data.sql
```

## 🔄 Paso 6: Deploy

### 6.1 Deploy Manual

1. En tu Web Service, click en **"Manual Deploy"**
2. Selecciona **"Deploy latest commit"**
3. Espera a que termine el build (5-10 minutos)

### 6.2 Auto Deploy

Render automáticamente hace deploy cuando:
- Haces push a la rama `main` en GitHub
- Cambias variables de entorno
- Actualizas la configuración

### 6.3 Ver Logs

Para ver el progreso:
1. Click en **"Logs"** en el menú superior
2. Verás el build y deploy en tiempo real

## ✅ Paso 7: Verificar Deployment

### 7.1 URL de la Aplicación

Tu aplicación estará disponible en:
```
https://web-rehabsystem-1.onrender.com
```

### 7.2 Verificar Funcionamiento

1. Abre la URL en tu navegador
2. Deberías ver la página de login
3. Prueba con las credenciales:
   - Usuario: `admin`
   - Contraseña: `admin123`

### 7.3 Verificar Base de Datos

Desde el Shell de Render:
```bash
python scripts/verification/verificar_sistema.py
```

## 🐛 Solución de Problemas

### Error: "Application failed to start"

**Causa**: Problema con gunicorn o dependencias

**Solución**:
```bash
# Verificar requirements.txt incluye:
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Error: "Database connection failed"

**Causa**: DATABASE_URL incorrecta

**Solución**:
1. Verifica que DATABASE_URL esté configurada
2. Asegúrate de usar Internal Database URL
3. Verifica el fix de postgres:// a postgresql://

### Error: "Module not found"

**Causa**: Dependencia faltante

**Solución**:
```bash
# Agregar a requirements.txt y hacer commit
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### La aplicación es muy lenta

**Causa**: Plan Free tiene limitaciones

**Solución**:
- El plan Free "duerme" después de 15 min de inactividad
- Primera carga puede tardar 30-60 segundos
- Considera upgrade a plan Starter ($7/mes)

## 📊 Monitoreo

### Métricas Disponibles

En el Dashboard de Render:
- **CPU Usage**: Uso de CPU
- **Memory Usage**: Uso de memoria
- **Response Time**: Tiempo de respuesta
- **Request Count**: Número de requests

### Logs

Para ver logs en tiempo real:
```bash
# Desde Render Dashboard
Click en "Logs" → Ver logs en tiempo real

# Filtrar logs
Click en el ícono de filtro para buscar errores
```

## 🔒 Seguridad

### Recomendaciones:

1. **Cambiar SECRET_KEY**: Usa una clave única y segura
2. **Cambiar Contraseñas**: Cambia las contraseñas por defecto
3. **HTTPS**: Render proporciona HTTPS automáticamente
4. **Variables de Entorno**: Nunca hagas commit de .env
5. **Backups**: Render hace backups automáticos de la BD

## 💰 Costos

### Plan Free:
- Web Service: Gratis
- PostgreSQL: Gratis (90 días, luego $7/mes)
- Limitaciones:
  - 750 horas/mes
  - Duerme después de 15 min inactividad
  - 512 MB RAM

### Plan Starter:
- Web Service: $7/mes
- PostgreSQL: $7/mes
- Total: $14/mes
- Sin limitaciones de sleep
- 512 MB RAM

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Render PostgreSQL](https://render.com/docs/databases)
- [Deploy Flask en Render](https://render.com/docs/deploy-flask)

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Consulta la documentación de Render
4. Abre un issue en GitHub
