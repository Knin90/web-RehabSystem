# ⚡ Configuración Rápida - RehabSystem en Render

## 🎯 Guía Rápida (5 minutos)

### 1️⃣ Crear Base de Datos (2 min)

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configurar:
   - Name: `rehab-db`
   - Database: `rehab_system`
   - User: `rehab_user`
   - Region: Oregon (US West)
4. Click **"Create Database"**
5. **Guardar** el Internal Database URL

### 2️⃣ Crear Web Service (2 min)

1. Click **"New +"** → **"Web Service"**
2. Conectar GitHub: `web-RehabSystem`
3. Configurar:
   - Name: `web-rehabsystem-1`
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app --bind 0.0.0.0:$PORT`

### 3️⃣ Variables de Entorno (1 min)

En **"Environment"**, agregar:

```bash
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=<generar-clave-segura>
DATABASE_URL=<conectar-base-de-datos>
```

**Generar SECRET_KEY**:
```python
import secrets
print(secrets.token_hex(32))
```

**DATABASE_URL**: Click en ícono de enlace → Seleccionar `rehab-db`

### 4️⃣ Deploy y Verificar (5-10 min)

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Esperar build (5-10 min)
3. Abrir URL: `https://web-rehabsystem-1.onrender.com`

### 5️⃣ Inicializar Base de Datos

**Opción A - Desde Render Shell**:
```bash
python scripts/setup/setup_complete.py
```

**Opción B - Desde tu computadora**:
```bash
psql <EXTERNAL_DATABASE_URL> < scripts/sql/schema.sql
psql <EXTERNAL_DATABASE_URL> < scripts/sql/seed_data.sql
```

## ✅ Verificar Funcionamiento

1. Abrir: `https://web-rehabsystem-1.onrender.com`
2. Login con:
   - Usuario: `admin`
   - Contraseña: `admin123`

## 📚 Documentación Completa

- **Guía Detallada**: `docs/CONFIGURACION_RENDER.md`
- **Scripts SQL**: `scripts/sql/README.md`
- **Resumen**: `docs/RESUMEN_CONFIGURACION.md`

## 🆘 Problemas Comunes

### App no inicia
```bash
# Verificar requirements.txt incluye:
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Error de base de datos
```bash
# Verificar DATABASE_URL en Environment
# Ejecutar: python scripts/setup/setup_complete.py
```

### App muy lenta
- Plan Free "duerme" después de 15 min
- Primera carga tarda 30-60 segundos
- Considera upgrade a Starter ($7/mes)

## 💡 Tips

- ✅ Usa Internal Database URL (más rápido)
- ✅ Misma región para BD y Web Service
- ✅ Cambia contraseñas por defecto
- ✅ Revisa logs en Render Dashboard
- ✅ Habilita auto-deploy desde GitHub

---

**¿Necesitas ayuda?** Ver `docs/CONFIGURACION_RENDER.md` para guía completa
