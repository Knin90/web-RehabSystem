# 🚀 Setup para Producción (Render)

## Problema Actual
Las rutinas no muestran ejercicios porque **los ejercicios base no existen en la BD de producción**.

## Solución

### Paso 1: Ejecutar Script de Inicialización

#### Opción A: Desde Render Shell
1. Ve a tu dashboard de Render: https://dashboard.render.com
2. Selecciona tu servicio `web-RehabSystem`
3. Click en "Shell" en el menú lateral
4. Ejecuta:
```bash
python init_production_data.py
```

#### Opción B: Agregar a Build Command
En Render, actualiza el "Build Command":
```bash
pip install -r requirements.txt && python init_production_data.py
```

### Paso 2: Verificar Ejercicios
Después de ejecutar el script, verifica:
```bash
python -c "from app import create_app; from app.models import Exercise; app = create_app(); app.app_context().push(); print(f'Ejercicios: {Exercise.query.count()}')"
```

Debería mostrar: `Ejercicios: 8`

### Paso 3: Crear Rutina como Terapeuta
1. Login como terapeuta en producción
2. Ir a "Rutinas"
3. Click en "Nueva rutina"
4. **IMPORTANTE**: Agregar ejercicios de la biblioteca
5. Guardar rutina
6. Asignar a paciente

### Paso 4: Verificar como Paciente
1. Login como paciente
2. Ir a "Mis Rutinas"
3. Click en "Ver Detalles"
4. ✅ Deberías ver los ejercicios

## Verificación de Problemas

### Si no aparecen ejercicios en el modal:
1. Abre consola del navegador (F12)
2. Busca el log: `✓ Ejercicios: Array(X)`
3. Si X = 0, la rutina no tiene ejercicios asociados

### Causas comunes:
- ❌ Los ejercicios (IDs 1-8) no existen en BD
- ❌ La rutina se creó sin agregar ejercicios
- ❌ El endpoint `create-routine` falló silenciosamente

### Solución:
```bash
# En Render Shell:
python init_production_data.py
```

Luego crear una nueva rutina con ejercicios.

## Variables de Entorno en Render

Asegúrate de tener configuradas:
```
DATABASE_URL=postgresql://...
SECRET_KEY=tu_clave_secreta
FLASK_ENV=production
```

## Migraciones

Si necesitas ejecutar migraciones:
```bash
# En Render Shell:
python migrate_add_routines.py
```

## Logs Útiles

### Ver ejercicios en BD:
```bash
python -c "from app import create_app; from app.models import Exercise; app = create_app(); app.app_context().push(); [print(f'{e.id}: {e.name}') for e in Exercise.query.all()]"
```

### Ver rutinas:
```bash
python list_all_routines.py
```

### Ver pacientes y sus rutinas:
```bash
python check_user_routines.py
```

## Troubleshooting

### Error: "Rutina no encontrada" (404)
- La rutina no está asignada al paciente correcto
- Verifica con: `python check_user_routines.py`

### Error: "No hay ejercicios en esta rutina"
- La rutina existe pero no tiene ejercicios
- Ejecuta: `python init_production_data.py`
- Crea una nueva rutina con ejercicios

### Error: "Exercise ID X not found"
- Los ejercicios no existen en BD
- Ejecuta: `python init_production_data.py`

## Resumen

1. ✅ Ejecutar `init_production_data.py` en Render
2. ✅ Crear rutina como terapeuta (con ejercicios)
3. ✅ Asignar a paciente
4. ✅ Verificar como paciente

---

**Nota**: El código está 100% funcional. Solo necesitas inicializar los datos en producción.
