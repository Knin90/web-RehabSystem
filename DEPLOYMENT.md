# 🚀 Guía de Deployment - RehabSystem

## ⚠️ Importante sobre Netlify

**Netlify NO soporta aplicaciones Flask/Python**. Netlify es solo para sitios estáticos (HTML, CSS, JavaScript).

Para desplegar RehabSystem necesitas una plataforma que soporte Python y Flask.

---

## 🎯 Opciones Recomendadas

### 1. 🟢 Render.com (RECOMENDADO - Gratis)

#### Ventajas:
- ✅ Plan gratuito permanente
- ✅ Deploy automático desde GitHub
- ✅ Base de datos PostgreSQL incluida
- ✅ SSL/HTTPS automático
- ✅ Muy fácil de usar

#### Pasos para Deploy en Render:

1. **Crear cuenta en Render**
   - Ve a https://render.com
   - Regístrate con GitHub

2. **Conectar repositorio**
   - Click en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona `web-RehabSystem`

3. **Configurar el servicio**
   ```
   Name: rehab-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn run:app
   ```

4. **Agregar variables de entorno**
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   FLASK_ENV=production
   DATABASE_URL=(se genera automáticamente)
   ```

5. **Crear base de datos PostgreSQL**
   - En el dashboard, click "New +"
   - Selecciona "PostgreSQL"
   - Nombre: `rehab-db`
   - Conecta con tu web service

6. **Deploy**
   - Click "Create Web Service"
   - Espera 5-10 minutos
   - ¡Listo! Tu app estará en: `https://rehab-system.onrender.com`

---

### 2. 🚂 Railway.app (Muy Fácil)

#### Ventajas:
- ✅ Deploy en 1 click
- ✅ $5 de crédito gratis mensual
- ✅ Muy rápido

#### Pasos:

1. **Ir a Railway**
   - https://railway.app
   - Login con GitHub

2. **Nuevo Proyecto**
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configurar**
   - Railway detecta Flask automáticamente
   - Agrega PostgreSQL desde "Add Plugin"

4. **Variables de entorno**
   ```
   SECRET_KEY=tu-clave-secreta
   FLASK_ENV=production
   ```

5. **Deploy automático**
   - Railway hace deploy automáticamente
   - URL: `https://tu-app.up.railway.app`

---

### 3. 🐍 PythonAnywhere (Especializado)

#### Ventajas:
- ✅ Especializado en Python/Flask
- ✅ Plan gratuito disponible
- ✅ Muy estable

#### Pasos:

1. **Crear cuenta**
   - https://www.pythonanywhere.com
   - Plan gratuito (Beginner)

2. **Subir código**
   - Desde consola Bash:
   ```bash
   git clone https://github.com/Knin90/web-RehabSystem.git
   cd web-RehabSystem
   ```

3. **Crear virtualenv**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 rehab-env
   pip install -r requirements.txt
   ```

4. **Configurar Web App**
   - Web tab → Add a new web app
   - Manual configuration → Python 3.10
   - WSGI file: apuntar a `run.py`

5. **Configurar base de datos**
   - Databases tab → Initialize MySQL
   - Actualizar DATABASE_URL

---

### 4. 🔴 Heroku (Clásico - Ya no gratis)

#### Nota: Heroku eliminó su plan gratuito en 2022

Si tienes presupuesto ($7/mes):

1. **Instalar Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Crear app**
   ```bash
   cd web-RehabSystem
   heroku create rehab-system
   ```

4. **Agregar PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**
   ```bash
   git push heroku version-2:main
   ```

---

## 📋 Archivos Necesarios (Ya Creados)

✅ `requirements.txt` - Dependencias (con gunicorn y psycopg2)
✅ `Procfile` - Comando de inicio
✅ `render.yaml` - Configuración para Render
✅ `run.py` - Modificado para producción

---

## 🔧 Configuración de Producción

### Variables de Entorno Necesarias:

```bash
SECRET_KEY=clave-super-secreta-cambiar-en-produccion
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Generar SECRET_KEY segura:

```python
import secrets
print(secrets.token_hex(32))
```

---

## 🗄️ Migración de Base de Datos

Después del deploy, ejecutar:

```bash
# En Render/Railway (desde la consola web)
flask db upgrade
python seed_data.py
```

---

## ✅ Checklist Pre-Deploy

- [ ] Código subido a GitHub
- [ ] `requirements.txt` actualizado con gunicorn
- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL creada
- [ ] SECRET_KEY generada
- [ ] Debug mode = False en producción
- [ ] Credenciales de prueba cambiadas

---

## 🎯 Recomendación Final

**Para RehabSystem, usa Render.com:**

1. Es gratis
2. Muy fácil de configurar
3. Deploy automático desde GitHub
4. Incluye PostgreSQL gratis
5. SSL/HTTPS automático

**URL de ejemplo:** `https://rehab-system.onrender.com`

---

## 🆘 Troubleshooting

### Error: "Application failed to start"
- Verifica que `gunicorn` esté en requirements.txt
- Revisa los logs en el dashboard

### Error: "Database connection failed"
- Verifica DATABASE_URL en variables de entorno
- Asegúrate de tener PostgreSQL conectado

### Error: "Module not found"
- Ejecuta `pip freeze > requirements.txt`
- Asegúrate de incluir todas las dependencias

---

## 📞 Soporte

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **PythonAnywhere:** https://help.pythonanywhere.com

---

**Última actualización:** Diciembre 2024
**Versión:** 2.0.0
