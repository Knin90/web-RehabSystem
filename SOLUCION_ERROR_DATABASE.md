# 🔧 Solución: Error "no such table: user"

## 🚨 Problema Detectado

El servicio en Render está funcionando pero la base de datos no está inicializada:
```
sqlite3.OperationalError: no such table: user
```

## 🔍 Causa

El archivo `render.yaml` estaba ejecutando directamente `gunicorn` sin pasar por el script `start.sh` que inicializa la base de datos.

## ✅ Solución Aplicada

### 1. Corregido `render.yaml`
```yaml
startCommand: bash start.sh  # ← Cambiado de "gunicorn run:app"
```

### 2. Corregido `init_db_auto.py`
- Arreglado error de indentación en línea 30

### 3. Agregada variable de entorno
```yaml
- key: FLASK_ENV
  value: production
```

## 🚀 Pasos para Aplicar la Solución

### Opción 1: Desde GitHub (Recomendado)

1. **Subir cambios a GitHub**:
```bash
cd web-RehabSystem
git add .
git commit -m "fix: Corregir inicialización de base de datos en Render"
git push origin main
```

2. **Render detectará los cambios automáticamente** y redesplegará

3. **Verificar logs en Render**:
   - Ir a https://dashboard.render.com
   - Seleccionar el servicio "rehab-system"
   - Ver logs en tiempo real
   - Buscar: "✓ Tablas creadas/verificadas"

### Opción 2: Desde Dashboard de Render

1. **Ir a Render Dashboard**:
   - https://dashboard.render.com

2. **Seleccionar el servicio**:
   - Click en "rehab-system"

3. **Manual Deploy**:
   - Click en "Manual Deploy"
   - Seleccionar "Clear build cache & deploy"

4. **Monitorear logs**:
   - Ver la pestaña "Logs"
   - Esperar a ver: "✓ Tablas creadas/verificadas"

## 📊 Verificación

### Logs Esperados (Correctos):
```
==========================================
INICIANDO REHABSYSTEM
==========================================

Paso 1: Verificando variables de entorno...
FLASK_ENV: production
DATABASE_URL: postgresql://...

Paso 2: Inicializando base de datos...
Importando módulos...
Creando aplicación...
Inicializando contexto...
Creando tablas...
✓ Tablas creadas/verificadas
Verificando datos existentes...
Usuarios encontrados: 0
Base de datos vacía. Creando datos iniciales...
✓ Datos iniciales creados
  - Admin: admin / admin123
  - Terapeuta: terapeuta / tera123
  - Paciente: paciente / paci123

Paso 3: Iniciando gunicorn...
==========================================
[INFO] Starting gunicorn...
```

### Logs de Error (Antes):
```
sqlite3.OperationalError: no such table: user
```

## 🎯 Resultado Esperado

Después del redespliegue:
- ✅ Base de datos inicializada
- ✅ Tablas creadas
- ✅ Usuarios de prueba creados
- ✅ Aplicación funcionando correctamente

## 🔐 Credenciales de Prueba

Una vez desplegado, puedes acceder con:

**Admin**:
- Usuario: `admin`
- Contraseña: `admin123`

**Terapeuta**:
- Usuario: `terapeuta`
- Contraseña: `tera123`

**Paciente**:
- Usuario: `paciente`
- Contraseña: `paci123`

## 🐛 Si el Problema Persiste

### 1. Verificar DATABASE_URL
En el dashboard de Render:
- Settings → Environment
- Verificar que `DATABASE_URL` esté configurada
- Debe empezar con `postgresql://`

### 2. Verificar Base de Datos
- Ir a la pestaña "Databases"
- Verificar que "rehab-db" esté activa
- Estado debe ser "Available"

### 3. Logs Detallados
Ejecutar en la shell de Render:
```bash
python init_db_auto.py
```

### 4. Recrear Base de Datos (Último Recurso)
⚠️ **Esto borrará todos los datos**:
1. Dashboard → Databases → rehab-db
2. Settings → Delete Database
3. Crear nueva base de datos
4. Redesplegar el servicio

## 📞 Soporte

Si el problema continúa:
1. Copiar los logs completos
2. Verificar que todos los archivos estén en GitHub
3. Verificar que el commit se haya subido correctamente

## ✅ Checklist

- [ ] Archivos corregidos localmente
- [ ] Cambios subidos a GitHub
- [ ] Render ha detectado los cambios
- [ ] Redespliegue iniciado
- [ ] Logs muestran "✓ Tablas creadas/verificadas"
- [ ] Aplicación accesible en https://web-rehabsystem-1.onrender.com
- [ ] Login funciona correctamente

---

**Fecha**: 8 de Diciembre, 2025
**Estado**: Solución lista para aplicar
