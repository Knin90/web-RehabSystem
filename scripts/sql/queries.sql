-- ============================================
-- CONSULTAS SQL ÚTILES - REHABSYSTEM
-- ============================================

-- ============================================
-- CONSULTAS DE VERIFICACIÓN
-- ============================================

-- Ver todos los usuarios
SELECT id, nombre_usuario, correo_electronico, rol, esta_activo, fecha_creacion
FROM "user"
ORDER BY id;

-- Ver todos los pacientes con su usuario
SELECT 
    p.id,
    p.nombre_completo,
    u.nombre_usuario,
    u.correo_electronico,
    p.diagnostico,
    p.progreso,
    p.sesiones_completadas,
    p.sesiones_totales
FROM patient p
JOIN "user" u ON p.id_usuario = u.id
ORDER BY p.id;

-- Ver todos los terapeutas
SELECT 
    t.id,
    t.nombre_completo,
    u.nombre_usuario,
    t.especialidad,
    t.total_pacientes
FROM therapist t
JOIN "user" u ON t.id_usuario = u.id;

-- ============================================
-- CONSULTAS DE RUTINAS
-- ============================================

-- Ver rutinas con terapeuta y paciente
SELECT 
    r.id,
    r.nombre,
    t.nombre_completo as terapeuta,
    p.nombre_completo as paciente,
    r.duracion_minutos,
    r.dificultad,
    r.esta_activa
FROM routine r
JOIN therapist t ON r.id_terapeuta = t.id
LEFT JOIN patient p ON r.id_paciente = p.id
ORDER BY r.id;

-- Ver ejercicios de una rutina específica
SELECT 
    re.orden,
    e.nombre,
    e.descripcion,
    re.series,
    re.repeticiones,
    re.segundos_descanso,
    re.notas
FROM routine_exercise re
JOIN exercise e ON re.id_ejercicio = e.id
WHERE re.id_rutina = 1  -- Cambiar ID según necesidad
ORDER BY re.orden;

-- Ver todas las rutinas con conteo de ejercicios
SELECT 
    r.id,
    r.nombre,
    t.nombre_completo as terapeuta,
    p.nombre_completo as paciente,
    COUNT(re.id) as total_ejercicios
FROM routine r
JOIN therapist t ON r.id_terapeuta = t.id
LEFT JOIN patient p ON r.id_paciente = p.id
LEFT JOIN routine_exercise re ON r.id = re.id_rutina
GROUP BY r.id, r.nombre, t.nombre_completo, p.nombre_completo
ORDER BY r.id;

-- ============================================
-- CONSULTAS DE PACIENTES ASIGNADOS
-- ============================================

-- Ver pacientes asignados a un terapeuta (a través de rutinas)
SELECT DISTINCT
    p.id,
    p.nombre_completo,
    p.diagnostico,
    p.progreso,
    COUNT(r.id) as total_rutinas
FROM patient p
JOIN routine r ON p.id = r.id_paciente
WHERE r.id_terapeuta = 1  -- Cambiar ID del terapeuta
GROUP BY p.id, p.nombre_completo, p.diagnostico, p.progreso
ORDER BY p.nombre_completo;

-- Ver todos los pacientes con su terapeuta
SELECT 
    p.nombre_completo as paciente,
    t.nombre_completo as terapeuta,
    COUNT(r.id) as rutinas_asignadas
FROM patient p
LEFT JOIN routine r ON p.id = r.id_paciente
LEFT JOIN therapist t ON r.id_terapeuta = t.id
GROUP BY p.nombre_completo, t.nombre_completo
ORDER BY p.nombre_completo;

-- ============================================
-- CONSULTAS DE VIDEOS
-- ============================================

-- Ver todas las capturas de video
SELECT 
    sc.id,
    sc.tipo_captura,
    sc.nombre_archivo,
    COALESCE(t.nombre_completo, 'N/A') as terapeuta,
    COALESCE(p.nombre_completo, 'N/A') as paciente,
    sc.duracion,
    sc.es_permanente,
    sc.fecha_sesion
FROM session_capture sc
LEFT JOIN therapist t ON sc.id_terapeuta = t.id
LEFT JOIN patient p ON sc.id_paciente = p.id
WHERE sc.tipo_captura = 'video'
ORDER BY sc.fecha_sesion DESC;

-- Ver videos compartidos
SELECT 
    vs.id,
    t.nombre_completo as terapeuta,
    p.nombre_completo as paciente,
    sc.nombre_archivo,
    vs.mensaje,
    vs.leido,
    vs.fecha_compartido,
    vs.fecha_leido
FROM video_share vs
JOIN therapist t ON vs.id_terapeuta = t.id
JOIN patient p ON vs.id_paciente = p.id
JOIN session_capture sc ON vs.id_captura = sc.id
ORDER BY vs.fecha_compartido DESC;

-- Videos no leídos por paciente
SELECT 
    vs.id,
    t.nombre_completo as terapeuta,
    sc.nombre_archivo,
    vs.mensaje,
    vs.fecha_compartido
FROM video_share vs
JOIN therapist t ON vs.id_terapeuta = t.id
JOIN session_capture sc ON vs.id_captura = sc.id
WHERE vs.id_paciente = 1  -- Cambiar ID del paciente
  AND vs.leido = FALSE
ORDER BY vs.fecha_compartido DESC;

-- ============================================
-- CONSULTAS DE CITAS
-- ============================================

-- Ver citas programadas
SELECT 
    a.id,
    p.nombre_completo as paciente,
    t.nombre_completo as terapeuta,
    a.fecha,
    a.estado
FROM appointment a
JOIN patient p ON a.id_paciente = p.id
JOIN therapist t ON a.id_terapeuta = t.id
WHERE a.estado = 'programada'
ORDER BY a.fecha;

-- Citas por terapeuta
SELECT 
    t.nombre_completo as terapeuta,
    COUNT(a.id) as total_citas,
    SUM(CASE WHEN a.estado = 'programada' THEN 1 ELSE 0 END) as programadas,
    SUM(CASE WHEN a.estado = 'completada' THEN 1 ELSE 0 END) as completadas,
    SUM(CASE WHEN a.estado = 'cancelada' THEN 1 ELSE 0 END) as canceladas
FROM therapist t
LEFT JOIN appointment a ON t.id = a.id_terapeuta
GROUP BY t.nombre_completo;

-- ============================================
-- CONSULTAS DE ESTADÍSTICAS
-- ============================================

-- Resumen general del sistema
SELECT 
    (SELECT COUNT(*) FROM "user") as total_usuarios,
    (SELECT COUNT(*) FROM patient) as total_pacientes,
    (SELECT COUNT(*) FROM therapist) as total_terapeutas,
    (SELECT COUNT(*) FROM exercise) as total_ejercicios,
    (SELECT COUNT(*) FROM routine) as total_rutinas,
    (SELECT COUNT(*) FROM session_capture WHERE tipo_captura = 'video') as total_videos,
    (SELECT COUNT(*) FROM video_share) as videos_compartidos;

-- Progreso promedio de pacientes
SELECT 
    AVG(progreso) as progreso_promedio,
    MIN(progreso) as progreso_minimo,
    MAX(progreso) as progreso_maximo,
    AVG(sesiones_completadas * 100.0 / NULLIF(sesiones_totales, 0)) as porcentaje_sesiones
FROM patient;

-- Ejercicios más usados en rutinas
SELECT 
    e.nombre,
    e.categoria,
    COUNT(re.id) as veces_usado
FROM exercise e
LEFT JOIN routine_exercise re ON e.id = re.id_ejercicio
GROUP BY e.nombre, e.categoria
ORDER BY veces_usado DESC;

-- ============================================
-- CONSULTAS DE MANTENIMIENTO
-- ============================================

-- Ver tamaño de las tablas (PostgreSQL)
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ver índices de una tabla
SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'user'  -- Cambiar nombre de tabla
ORDER BY indexname;

-- Ver configuraciones del sistema
SELECT clave, valor, fecha_actualizacion
FROM system_settings
ORDER BY clave;

-- ============================================
-- CONSULTAS DE LIMPIEZA
-- ============================================

-- Eliminar videos antiguos (más de 90 días)
DELETE FROM session_capture
WHERE tipo_captura = 'video'
  AND es_permanente = FALSE
  AND fecha_sesion < CURRENT_TIMESTAMP - INTERVAL '90 days';

-- Eliminar videos compartidos ya leídos (más de 30 días)
DELETE FROM video_share
WHERE leido = TRUE
  AND fecha_leido < CURRENT_TIMESTAMP - INTERVAL '30 days';

-- Limpiar citas canceladas antiguas
DELETE FROM appointment
WHERE estado = 'cancelada'
  AND fecha < CURRENT_TIMESTAMP - INTERVAL '180 days';

-- ============================================
-- CONSULTAS DE ACTUALIZACIÓN
-- ============================================

-- Actualizar progreso de un paciente
UPDATE patient
SET progreso = (sesiones_completadas * 100.0 / NULLIF(sesiones_totales, 0))
WHERE id = 1;  -- Cambiar ID

-- Actualizar total de pacientes de un terapeuta
UPDATE therapist t
SET total_pacientes = (
    SELECT COUNT(DISTINCT r.id_paciente)
    FROM routine r
    WHERE r.id_terapeuta = t.id
      AND r.id_paciente IS NOT NULL
)
WHERE id = 1;  -- Cambiar ID

-- Marcar video como leído
UPDATE video_share
SET leido = TRUE,
    fecha_leido = CURRENT_TIMESTAMP
WHERE id = 1;  -- Cambiar ID

-- Desactivar rutinas antiguas
UPDATE routine
SET esta_activa = FALSE
WHERE fecha_creacion < CURRENT_TIMESTAMP - INTERVAL '365 days'
  AND esta_activa = TRUE;

-- ============================================
-- CONSULTAS DE BÚSQUEDA
-- ============================================

-- Buscar paciente por nombre
SELECT 
    p.id,
    p.nombre_completo,
    u.nombre_usuario,
    p.diagnostico,
    p.progreso
FROM patient p
JOIN "user" u ON p.id_usuario = u.id
WHERE p.nombre_completo ILIKE '%andrea%'  -- Cambiar nombre
ORDER BY p.nombre_completo;

-- Buscar ejercicios por categoría
SELECT nombre, descripcion, repeticiones
FROM exercise
WHERE categoria = 'lower'  -- Cambiar categoría
ORDER BY nombre;

-- Buscar rutinas activas de un paciente
SELECT 
    r.nombre,
    r.descripcion,
    r.duracion_minutos,
    r.dificultad,
    COUNT(re.id) as total_ejercicios
FROM routine r
LEFT JOIN routine_exercise re ON r.id = re.id_rutina
WHERE r.id_paciente = 1  -- Cambiar ID
  AND r.esta_activa = TRUE
GROUP BY r.id, r.nombre, r.descripcion, r.duracion_minutos, r.dificultad;

-- ============================================
-- FIN DE CONSULTAS
-- ============================================
