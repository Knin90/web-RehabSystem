-- ============================================
-- REHABSYSTEM - DATOS INICIALES
-- Datos de prueba para desarrollo
-- ============================================

-- ============================================
-- USUARIOS
-- Contraseñas encriptadas con bcrypt
-- ============================================

-- Admin: admin / admin123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('admin', 'admin@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'admin', TRUE);

-- Terapeuta: terapeuta / tera123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('terapeuta', 'tera@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'therapist', TRUE);

-- Paciente 1: paciente / paci123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('paciente', 'paci@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'patient', TRUE);

-- Paciente 2: maria_garcia / maria123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('maria_garcia', 'maria.garcia@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'patient', TRUE);

-- Paciente 3: juan_perez / juan123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('juan_perez', 'juan.perez@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'patient', TRUE);

-- Paciente 4: carlos_rodriguez / carlos123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('carlos_rodriguez', 'carlos.rodriguez@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'patient', TRUE);

-- Paciente 5: sofia_martinez / sofia123
INSERT INTO "user" (nombre_usuario, correo_electronico, contrasena_encriptada, rol, esta_activo)
VALUES ('sofia_martinez', 'sofia.martinez@rehab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7Iq', 'patient', TRUE);

-- ============================================
-- TERAPEUTA
-- ============================================
INSERT INTO therapist (id_usuario, nombre_completo, especialidad, total_pacientes)
VALUES (2, 'Rafael Lu', 'Fisioterapeuta', 5);

-- ============================================
-- PACIENTES
-- ============================================
INSERT INTO patient (id_usuario, nombre_completo, diagnostico, progreso, sesiones_totales, sesiones_completadas)
VALUES 
(3, 'Andrea Luna', 'Rehabilitación rodilla', 75.0, 16, 12),
(4, 'María García', 'Lesión de hombro', 25.0, 20, 5),
(5, 'Juan Pérez', 'Rehabilitación de cadera', 53.3, 15, 8),
(6, 'Carlos Rodríguez', 'Lesión lumbar', 16.7, 18, 3),
(7, 'Sofía Martínez', 'Rehabilitación de tobillo', 83.3, 12, 10);

-- ============================================
-- EJERCICIOS
-- ============================================
INSERT INTO exercise (nombre, descripcion, categoria, repeticiones)
VALUES 
('Flexiones de rodilla', 'Ejercicio para fortalecer las rodillas', 'lower', '3x15'),
('Elevaciones de pierna', 'Ejercicio para fortalecer piernas', 'lower', '3x12'),
('Estiramientos lumbares', 'Ejercicio para estirar la zona lumbar', 'lower', '4x30s'),
('Rotación de hombros', 'Ejercicio para movilidad de hombros', 'upper', '3x10'),
('Flexiones de brazo', 'Ejercicio para fortalecer brazos', 'upper', '3x8'),
('Plancha abdominal', 'Ejercicio para fortalecer core', 'core', '3x30s'),
('Sentadillas asistidas', 'Ejercicio para fortalecer piernas', 'lower', '3x12'),
('Puente de glúteos', 'Ejercicio para fortalecer glúteos', 'lower', '3x15');

-- ============================================
-- RUTINAS
-- Asignar rutinas a cada paciente
-- ============================================

-- Rutina para Andrea Luna (Rodilla)
INSERT INTO routine (nombre, descripcion, id_terapeuta, id_paciente, duracion_minutos, dificultad, esta_activa)
VALUES ('Rutina de Andrea Luna', 'Rutina personalizada para Rehabilitación rodilla', 1, 1, 30, 'media', TRUE);

-- Rutina para María García (Hombro)
INSERT INTO routine (nombre, descripcion, id_terapeuta, id_paciente, duracion_minutos, dificultad, esta_activa)
VALUES ('Rutina de María García', 'Rutina personalizada para Lesión de hombro', 1, 2, 30, 'media', TRUE);

-- Rutina para Juan Pérez (Cadera)
INSERT INTO routine (nombre, descripcion, id_terapeuta, id_paciente, duracion_minutos, dificultad, esta_activa)
VALUES ('Rutina de Juan Pérez', 'Rutina personalizada para Rehabilitación de cadera', 1, 3, 30, 'media', TRUE);

-- Rutina para Carlos Rodríguez (Lumbar)
INSERT INTO routine (nombre, descripcion, id_terapeuta, id_paciente, duracion_minutos, dificultad, esta_activa)
VALUES ('Rutina de Carlos Rodríguez', 'Rutina personalizada para Lesión lumbar', 1, 4, 30, 'media', TRUE);

-- Rutina para Sofía Martínez (Tobillo)
INSERT INTO routine (nombre, descripcion, id_terapeuta, id_paciente, duracion_minutos, dificultad, esta_activa)
VALUES ('Rutina de Sofía Martínez', 'Rutina personalizada para Rehabilitación de tobillo', 1, 5, 30, 'media', TRUE);

-- ============================================
-- EJERCICIOS EN RUTINAS
-- Agregar 3 ejercicios a cada rutina
-- ============================================

-- Rutina 1 (Andrea Luna - Rodilla)
INSERT INTO routine_exercise (id_rutina, id_ejercicio, orden, series, repeticiones, segundos_descanso)
VALUES 
(1, 1, 0, 3, 10, 30),  -- Flexiones de rodilla
(1, 2, 1, 3, 10, 30),  -- Elevaciones de pierna
(1, 3, 2, 3, 10, 30);  -- Estiramientos lumbares

-- Rutina 2 (María García - Hombro)
INSERT INTO routine_exercise (id_rutina, id_ejercicio, orden, series, repeticiones, segundos_descanso)
VALUES 
(2, 4, 0, 3, 10, 30),  -- Rotación de hombros
(2, 5, 1, 3, 10, 30),  -- Flexiones de brazo
(2, 6, 2, 3, 10, 30);  -- Plancha abdominal

-- Rutina 3 (Juan Pérez - Cadera)
INSERT INTO routine_exercise (id_rutina, id_ejercicio, orden, series, repeticiones, segundos_descanso)
VALUES 
(3, 7, 0, 3, 10, 30),  -- Sentadillas asistidas
(3, 8, 1, 3, 10, 30),  -- Puente de glúteos
(3, 3, 2, 3, 10, 30);  -- Estiramientos lumbares

-- Rutina 4 (Carlos Rodríguez - Lumbar)
INSERT INTO routine_exercise (id_rutina, id_ejercicio, orden, series, repeticiones, segundos_descanso)
VALUES 
(4, 3, 0, 3, 10, 30),  -- Estiramientos lumbares
(4, 6, 1, 3, 10, 30),  -- Plancha abdominal
(4, 8, 2, 3, 10, 30);  -- Puente de glúteos

-- Rutina 5 (Sofía Martínez - Tobillo)
INSERT INTO routine_exercise (id_rutina, id_ejercicio, orden, series, repeticiones, segundos_descanso)
VALUES 
(5, 2, 0, 3, 10, 30),  -- Elevaciones de pierna
(5, 7, 1, 3, 10, 30),  -- Sentadillas asistidas
(5, 1, 2, 3, 10, 30);  -- Flexiones de rodilla

-- ============================================
-- CONFIGURACIONES DEL SISTEMA
-- ============================================
INSERT INTO system_settings (clave, valor)
VALUES 
('theme', 'light'),
('language', 'es'),
('session_duration', '45'),
('sessions_per_week', '3'),
('rest_time', '30'),
('email_notifications', 'on'),
('appointment_reminder', 'on'),
('progress_report', 'on'),
('detection_accuracy', '85'),
('realtime_analysis', 'on'),
('posture_correction', 'on'),
('capture_fps', '30');

-- ============================================
-- VERIFICACIÓN
-- ============================================

-- Contar registros
SELECT 'Usuarios' as tabla, COUNT(*) as total FROM "user"
UNION ALL
SELECT 'Terapeutas', COUNT(*) FROM therapist
UNION ALL
SELECT 'Pacientes', COUNT(*) FROM patient
UNION ALL
SELECT 'Ejercicios', COUNT(*) FROM exercise
UNION ALL
SELECT 'Rutinas', COUNT(*) FROM routine
UNION ALL
SELECT 'Ejercicios en Rutinas', COUNT(*) FROM routine_exercise
UNION ALL
SELECT 'Configuraciones', COUNT(*) FROM system_settings;

-- ============================================
-- FIN DE DATOS INICIALES
-- ============================================
