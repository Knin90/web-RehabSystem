# 📋 Feature: Vista de Rutinas para Pacientes

## Descripción
Los pacientes ahora pueden ver las rutinas de ejercicios que les han sido asignadas por su terapeuta, con detalles completos de cada ejercicio.

## Funcionalidades Implementadas

### 1. Nueva Opción en Menú del Paciente
**Archivo**: `templates/patient/base_paciente.html`

- ✅ Agregada opción "Mis Rutinas" con ícono de clipboard
- Ubicada entre "Historial" e "Iniciar Terapia"
- Ruta: `/patient/routines`

### 2. Ruta Backend para Rutinas del Paciente
**Archivo**: `app/routes.py`

```python
@app.route('/patient/routines')
@login_required
@role_required('patient')
def patient_routines():
    """Ver rutinas asignadas al paciente"""
```

**Características**:
- ✅ Obtiene rutinas asignadas al paciente actual
- ✅ Auto-crea perfil de paciente si no existe
- ✅ Manejo robusto de errores
- ✅ Pasa datos al template

### 3. Endpoint API para Detalles de Rutina
**Archivo**: `app/routes.py`

```python
@app.route('/api/get-routine-details/<int:routine_id>', methods=['GET'])
@login_required
@role_required('patient')
def get_routine_details(routine_id):
```

**Características**:
- ✅ Verifica que la rutina pertenezca al paciente
- ✅ Retorna información completa de la rutina
- ✅ Incluye lista de ejercicios ordenados
- ✅ Detalles: sets, repeticiones, descanso, notas

**Respuesta JSON**:
```json
{
  "success": true,
  "routine": {
    "id": 1,
    "name": "Rutina de Rehabilitación",
    "description": "Rutina de 30 minutos",
    "duration_minutes": 30,
    "difficulty": "medium",
    "exercises": [
      {
        "id": 1,
        "name": "Flexiones de rodilla",
        "sets": 3,
        "repetitions": 15,
        "rest_seconds": 30,
        "notes": "Mantener postura",
        "order": 0
      }
    ]
  }
}
```

### 4. Template de Vista de Rutinas
**Archivo**: `templates/patient/routines.html`

#### Características Visuales:
- ✅ **Cards responsivas** con diseño moderno
- ✅ **Íconos dinámicos** según dificultad (walking/dumbbell/running)
- ✅ **Badges de color** según dificultad (verde/amarillo/rojo)
- ✅ **Estadísticas visuales**: duración y cantidad de ejercicios
- ✅ **Hover effects** con elevación y sombra
- ✅ **Estado vacío** con mensaje amigable

#### Modal de Detalles:
- ✅ **Header con color** de marca
- ✅ **Lista de ejercicios** con información completa
- ✅ **Íconos descriptivos** para sets, repeticiones, descanso
- ✅ **Notas adicionales** si existen
- ✅ **Botón "Iniciar Rutina"** (preparado para futura funcionalidad)

#### JavaScript:
- ✅ **Event delegation** para mejor rendimiento
- ✅ **Fetch asíncrono** para cargar detalles
- ✅ **Manejo de errores** con alertas
- ✅ **Renderizado dinámico** del modal

## Flujo de Usuario

```
1. Paciente inicia sesión
   ↓
2. Click en "Mis Rutinas" en el menú
   ↓
3. Ve lista de rutinas asignadas (cards)
   ↓
4. Click en "Ver Detalles" de una rutina
   ↓
5. Fetch a /api/get-routine-details/{id}
   ↓
6. Modal muestra ejercicios completos
   ↓
7. Puede cerrar o "Iniciar Rutina"
```

## Diseño Visual

### Card de Rutina
```
┌─────────────────────────────┐
│ 🏃 Ícono        [Badge]     │
│                              │
│ Nombre de Rutina            │
│ Descripción breve...        │
│                              │
│ ┌────────────────────────┐  │
│ │ 🕐 30 min  📋 5 ejerc. │  │
│ └────────────────────────┘  │
│                              │
│ [Ver Detalles]              │
└─────────────────────────────┘
```

### Modal de Detalles
```
┌─────────────────────────────────┐
│ 📋 Nombre de Rutina        [X] │
├─────────────────────────────────┤
│ Descripción                     │
│ [30 min] [Medio]                │
│                                 │
│ Ejercicios:                     │
│ ┌─────────────────────────────┐ │
│ │ 1. Flexiones de rodilla     │ │
│ │ 🔄 3 series  # 15 reps      │ │
│ │ 🕐 30s descanso             │ │
│ └─────────────────────────────┘ │
│                                 │
│ [Cerrar] [Iniciar Rutina]      │
└─────────────────────────────────┘
```

## Estilos CSS

### Componentes Principales:
- `.card-custom` - Card con bordes redondeados y transiciones
- `.routine-icon` - Ícono circular con gradiente
- `.routine-stats` - Contenedor de estadísticas
- `.exercise-item` - Item de ejercicio con borde izquierdo
- `.exercise-details` - Detalles del ejercicio en línea

### Colores:
- **Gradiente principal**: `#667eea` → `#764ba2`
- **Fácil**: Verde (`bg-success`)
- **Medio**: Amarillo (`bg-warning`)
- **Difícil**: Rojo (`bg-danger`)

## Archivos Modificados/Creados

### Modificados:
1. `app/routes.py` (+60 líneas)
   - Ruta `/patient/routines`
   - Endpoint `/api/get-routine-details/<id>`

2. `templates/patient/base_paciente.html` (+5 líneas)
   - Agregada opción "Mis Rutinas" en menú

### Creados:
3. `templates/patient/routines.html` (+255 líneas)
   - Template completo con HTML, CSS y JavaScript

## Testing

### Casos de Prueba:
1. ✅ Paciente sin rutinas asignadas → Muestra mensaje vacío
2. ✅ Paciente con rutinas → Muestra cards
3. ✅ Click en "Ver Detalles" → Abre modal con ejercicios
4. ✅ Verificación de permisos → Solo el paciente dueño puede ver sus rutinas
5. ✅ Rutina inexistente → Error 404

### Para Probar:
```bash
1. Login como terapeuta
2. Ir a /therapist/routines
3. Crear rutina y asignar a paciente
4. Logout
5. Login como paciente
6. Ir a "Mis Rutinas"
7. Verificar que aparece la rutina
8. Click en "Ver Detalles"
9. Verificar ejercicios completos
```

## Próximas Mejoras

### Funcionalidades Futuras:
- 🔜 **Iniciar rutina**: Integrar con página de terapia
- 🔜 **Progreso de rutina**: Marcar ejercicios completados
- 🔜 **Historial**: Ver rutinas completadas
- 🔜 **Filtros**: Por dificultad, duración, fecha
- 🔜 **Búsqueda**: Buscar rutinas por nombre
- 🔜 **Favoritos**: Marcar rutinas favoritas
- 🔜 **Comentarios**: Feedback al terapeuta sobre rutinas

## Beneficios

- ✅ **Autonomía del paciente**: Puede revisar sus rutinas en cualquier momento
- ✅ **Claridad**: Información detallada de cada ejercicio
- ✅ **Motivación**: Visualización clara de su plan de rehabilitación
- ✅ **Accesibilidad**: Diseño responsive para móvil y desktop
- ✅ **UX moderna**: Interfaz intuitiva y atractiva

## Commit
```
feat: Agregar vista de rutinas para pacientes
- Los pacientes pueden ver rutinas asignadas por terapeuta con detalles completos
```

## Fecha
2 de diciembre de 2024
