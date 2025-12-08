# Actualizar Start Command en Render

## 🎯 Problema Resuelto

Sin acceso al Shell de Render (plan gratuito), necesitamos que la aplicación inicialice la base de datos automáticamente.

## ✅ Solución Implementada

Hemos creado:
1. **`init_db_auto.py`** - Script que inicializa la BD automáticamente
2. **`start.sh`** - Script que ejecuta init_db_auto.py antes de gunicorn

## 🔧 Actualizar Start Command en Render

### Paso 1: Ir a Settings

1. En Render Dashboard, ve a tu Web Service
2. Click en **"Settings"** (menú lateral izquierdo)
3. Scroll hasta **"Build & Deploy"**

### Paso 2: Cambiar Start Command

**Comando Anterior**:
```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

**Nuevo Comando**:
```bash
bash start.sh
```

O alternativamente:
```bash
python init_db_auto.py && gunicorn run:app --bind 0.0.0.0:$PORT
```

### Paso 3: Guardar y Redeploy

1. Click en **"Save Changes"**
2. Render hará redeploy automáticamente
3. Espera 5-10 minutos

## 📊 Qué Hace el Script

El script `init_db_auto.py`:

1. ✅ Crea todas las tablas si no existen
2. ✅ Verifica si hay datos
3. ✅ Si la BD está vacía, crea:
   - 1 Administrador (admin / admin123)
   - 1 Terapeuta (terapeuta / tera123)
   - 1 Paciente (paciente / paci123)
   - 3 Ejercicios básicos
   - Configuraciones del sistema
4. ✅ Si ya hay datos, no hace nada
5. ✅ Inicia gunicorn normalmente

## 🔍 Verificar en Logs

Después del redeploy, en los logs deberías ver:

```
Inicializando base de datos...
✓ Tablas creadas/verificadas
✓ Datos iniciales creados
  - Admin: admin / admin123
  - Terapeuta: terapeuta / tera123
  - Paciente: paciente / paci123
Iniciando gunicorn...
Starting gunicorn...
Listening at: http://0.0.0.0:10000
```

## 🎉 Resultado Esperado

Después del redeploy:
1. ✅ Base de datos inicializada automáticamente
2. ✅ Aplicación funcionando sin error 500
3. ✅ Puedes hacer login con admin/admin123

## 📝 Credenciales Creadas

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Terapeuta
- Usuario: `terapeuta`
- Contraseña: `tera123`

### Paciente
- Usuario: `paciente`
- Contraseña: `paci123`

## ⚠️ Importante

Este script:
- ✅ Es seguro ejecutar múltiples veces
- ✅ No duplica datos
- ✅ Solo crea datos si la BD está vacía
- ✅ No requiere Shell de Render

## 🔄 Alternativa sin start.sh

Si prefieres no usar start.sh, puedes usar directamente:

**Start Command**:
```bash
python init_db_auto.py && gunicorn run:app --bind 0.0.0.0:$PORT
```

Esto hace lo mismo:
1. Ejecuta `python init_db_auto.py` (inicializa BD)
2. Si tiene éxito, ejecuta `gunicorn run:app --bind 0.0.0.0:$PORT`

## 🎯 Próximos Pasos

1. ✅ Actualizar Start Command en Render Settings
2. ⏳ Esperar redeploy (5-10 min)
3. ⏳ Verificar logs
4. ✅ Probar aplicación: https://web-rehabsystem-1.onrender.com
5. ✅ Login con admin/admin123

---

**Nota**: Esta solución funciona sin necesidad del Shell de Render (plan gratuito)
