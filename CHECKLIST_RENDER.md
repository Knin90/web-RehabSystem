# ✅ Checklist de Configuración en Render

## 📊 Estado Actual de tu Configuración

Basado en la imagen que compartiste:

### Variables de Entorno Configuradas:
- ✅ `FLASK_APP = run.py`
- ✅ `FLASK_ENV = production`
- ❌ `SECRET_KEY` - **FALTA AGREGAR**
- ❌ `DATABASE_URL` - **FALTA CONECTAR**

## 🎯 Pasos Pendientes

### 1. Crear Base de Datos PostgreSQL (si no existe)

```
□ Ir a Render Dashboard
□ Click "New +" → "PostgreSQL"
□ Name: rehab-db
□ Database: rehab_system
□ User: rehab_user
□ Region: Oregon (US West)
□ Click "Create Database"
□ Esperar 2-3 minutos
```

### 2. Generar y Agregar SECRET_KEY

```
□ Generar clave:
  python -c "import secrets; print(secrets.token_hex(32))"

□ En Render Web Service:
  □ Ir a "Environment"
  □ Click "Add Environment Variable"
  □ Key: SECRET_KEY
  □ Value: <pegar-clave-generada>
  □ Click "Save Changes"
```

### 3. Conectar DATABASE_URL

```
□ En "Environment"
□ Click "Add Environment Variable"
□ Key: DATABASE_URL
□ Click en ícono de enlace (🔗)
□ Seleccionar: rehab-db
□ Property: Internal Database URL
□ Click "Save Changes"
```

### 4. Verificar Build & Start Commands

```
□ Ir a "Settings"
□ Build Command: pip install -r requirements.txt
□ Start Command: gunicorn run:app --bind 0.0.0.0:$PORT
```

### 5. Deploy

```
□ Render hará auto-deploy después de cambios
□ O click "Manual Deploy" → "Deploy latest commit"
□ Esperar 5-10 minutos
□ Ver logs en "Logs" tab
```

### 6. Inicializar Base de Datos

```
□ Cuando deploy termine exitosamente
□ Click en "Shell" (arriba)
□ Ejecutar: python scripts/setup/setup_complete.py
□ Verificar que se crearon usuarios y datos
```

### 7. Probar Aplicación

```
□ Abrir URL: https://web-rehabsystem-1.onrender.com
□ Debería ver página de login
□ Probar login:
  Usuario: admin
  Contraseña: admin123
```

## 🔍 Verificación de Configuración

### Variables de Entorno Completas:

```bash
✅ FLASK_APP=run.py
✅ FLASK_ENV=production
⚠️ SECRET_KEY=<64-caracteres-hexadecimales>
⚠️ DATABASE_URL=postgresql://rehab_user:password@dpg-xxxxx/rehab_system
```

### Archivos Verificados:

```
✅ requirements.txt - incluye gunicorn y psycopg2-binary
✅ app/config.py - tiene fix para PostgreSQL
✅ run.py - punto de entrada correcto
✅ Procfile - configurado con gunicorn
```

## 🚨 Errores Comunes

### Error 1: "Application failed to start"
**Causa**: Falta SECRET_KEY o DATABASE_URL
**Solución**: Agregar ambas variables

### Error 2: "Could not connect to database"
**Causa**: DATABASE_URL no conectada o incorrecta
**Solución**: Usar Internal Database URL con ícono de enlace

### Error 3: "Module 'gunicorn' not found"
**Causa**: requirements.txt no tiene gunicorn
**Solución**: Ya está en requirements.txt, hacer redeploy

### Error 4: "No module named 'psycopg2'"
**Causa**: Falta driver PostgreSQL
**Solución**: Ya está en requirements.txt (psycopg2-binary)

## 📝 Comandos Útiles

### Generar SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Ver logs en tiempo real:
```
Render Dashboard → Tu Web Service → Logs
```

### Conectar a base de datos:
```bash
# Desde Render Shell
psql $DATABASE_URL

# Desde tu computadora (usar External URL)
psql postgresql://rehab_user:password@dpg-xxxxx.oregon-postgres.render.com/rehab_system
```

### Inicializar base de datos:
```bash
# Desde Render Shell
python scripts/setup/setup_complete.py
```

## 🎯 Estado Final Esperado

Cuando todo esté configurado correctamente:

```
✅ Base de datos PostgreSQL creada y disponible
✅ Web Service con 4 variables de entorno
✅ Deploy exitoso (sin errores en logs)
✅ Aplicación accesible en URL
✅ Base de datos inicializada con datos
✅ Login funciona con admin/admin123
```

## 📞 Siguiente Paso

**AHORA MISMO**:
1. Genera SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Agrégala en Render Environment
3. Conecta DATABASE_URL desde la base de datos
4. Espera el redeploy automático
5. Verifica en logs que todo esté bien

## 📚 Documentación

- Guía completa: `docs/CONFIGURACION_RENDER.md`
- Variables de entorno: `docs/VARIABLES_ENTORNO_RENDER.md`
- Guía rápida: `CONFIGURACION_RAPIDA.md`

---

**¿Listo para continuar?** Sigue los pasos 2 y 3 arriba para completar la configuración.
