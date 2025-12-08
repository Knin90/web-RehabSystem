-- ============================================
-- REHABSYSTEM - ESQUEMA DE BASE DE DATOS
-- PostgreSQL / SQLite Compatible
-- ============================================

-- Eliminar tablas si existen (para reiniciar)
DROP TABLE IF EXISTS video_share CASCADE;
DROP TABLE IF EXISTS routine_exercise CASCADE;
DROP TABLE IF EXISTS routine CASCADE;
DROP TABLE IF EXISTS session_capture CASCADE;
DROP TABLE IF EXISTS system_settings CASCADE;
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS exercise CASCADE;
DROP TABLE IF EXISTS therapist CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS user CASCADE;

-- ============================================
-- TABLA: user
-- Usuarios del sistema (admin, therapist, patient)
-- ============================================
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(80) UNIQUE NOT NULL,
    correo_electronico VARCHAR(120) UNIQUE NOT NULL,
    contrasena_encriptada VARCHAR(128) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'therapist', 'patient')),
    esta_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_user_nombre_usuario ON user(nombre_usuario);
CREATE INDEX idx_user_rol ON user(rol);

-- ============================================
-- TABLA: patient
-- Información de pacientes
-- ============================================
CREATE TABLE patient (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER UNIQUE REFERENCES user(id) ON DELETE CASCADE,
    nombre_completo VARCHAR(200) NOT NULL,
    diagnostico TEXT,
    progreso FLOAT DEFAULT 0.0,
    sesiones_totales INTEGER DEFAULT 0,
    sesiones_completadas INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_patient_id_usuario ON patient(id_usuario);

-- ============================================
-- TABLA: therapist
-- Información de terapeutas
-- ============================================
CREATE TABLE therapist (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER UNIQUE REFERENCES user(id) ON DELETE CASCADE,
    nombre_completo VARCHAR(200) NOT NULL,
    especialidad VARCHAR(100),
    total_pacientes INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_therapist_id_usuario ON therapist(id_usuario);

-- ============================================
-- TABLA: exercise
-- Catálogo de ejercicios
-- ============================================
CREATE TABLE exercise (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    repeticiones VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_exercise_categoria ON exercise(categoria);

-- ============================================
-- TABLA: appointment
-- Citas entre pacientes y terapeutas
-- ============================================
CREATE TABLE appointment (
    id SERIAL PRIMARY KEY,
    id_paciente INTEGER REFERENCES patient(id) ON DELETE CASCADE,
    id_terapeuta INTEGER REFERENCES therapist(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL,
    estado VARCHAR(20) DEFAULT 'programada' CHECK (estado IN ('programada', 'completada', 'cancelada')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_appointment_paciente ON appointment(id_paciente);
CREATE INDEX idx_appointment_terapeuta ON appointment(id_terapeuta);
CREATE INDEX idx_appointment_fecha ON appointment(fecha);

-- ============================================
-- TABLA: system_settings
-- Configuraciones del sistema
-- ============================================
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor VARCHAR(500),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_system_settings_clave ON system_settings(clave);

-- ============================================
-- TABLA: session_capture
-- Capturas de fotos y videos de sesiones
-- ============================================
CREATE TABLE session_capture (
    id SERIAL PRIMARY KEY,
    id_terapeuta INTEGER REFERENCES therapist(id) ON DELETE SET NULL,
    id_paciente INTEGER REFERENCES patient(id) ON DELETE SET NULL,
    tipo_captura VARCHAR(20) NOT NULL CHECK (tipo_captura IN ('photo', 'video')),
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tamano_archivo INTEGER,
    duracion INTEGER,
    notas TEXT,
    fecha_sesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    es_permanente BOOLEAN DEFAULT FALSE,
    contiene_audio BOOLEAN DEFAULT FALSE
);

-- Índices
CREATE INDEX idx_session_capture_terapeuta ON session_capture(id_terapeuta);
CREATE INDEX idx_session_capture_paciente ON session_capture(id_paciente);
CREATE INDEX idx_session_capture_tipo ON session_capture(tipo_captura);
CREATE INDEX idx_session_capture_fecha ON session_capture(fecha_sesion);

-- ============================================
-- TABLA: routine
-- Rutinas de ejercicios
-- ============================================
CREATE TABLE routine (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    id_terapeuta INTEGER NOT NULL REFERENCES therapist(id) ON DELETE CASCADE,
    id_paciente INTEGER REFERENCES patient(id) ON DELETE CASCADE,
    duracion_minutos INTEGER DEFAULT 30,
    dificultad VARCHAR(20) DEFAULT 'media' CHECK (dificultad IN ('facil', 'media', 'dificil')),
    esta_activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_routine_terapeuta ON routine(id_terapeuta);
CREATE INDEX idx_routine_paciente ON routine(id_paciente);
CREATE INDEX idx_routine_activa ON routine(esta_activa);

-- ============================================
-- TABLA: routine_exercise
-- Ejercicios dentro de rutinas (tabla intermedia)
-- ============================================
CREATE TABLE routine_exercise (
    id SERIAL PRIMARY KEY,
    id_rutina INTEGER NOT NULL REFERENCES routine(id) ON DELETE CASCADE,
    id_ejercicio INTEGER NOT NULL REFERENCES exercise(id) ON DELETE CASCADE,
    orden INTEGER DEFAULT 0,
    series INTEGER DEFAULT 3,
    repeticiones INTEGER DEFAULT 10,
    segundos_descanso INTEGER DEFAULT 30,
    notas TEXT
);

-- Índices
CREATE INDEX idx_routine_exercise_rutina ON routine_exercise(id_rutina);
CREATE INDEX idx_routine_exercise_ejercicio ON routine_exercise(id_ejercicio);

-- ============================================
-- TABLA: video_share
-- Compartir videos entre terapeuta y paciente
-- ============================================
CREATE TABLE video_share (
    id SERIAL PRIMARY KEY,
    id_captura INTEGER NOT NULL REFERENCES session_capture(id) ON DELETE CASCADE,
    id_terapeuta INTEGER NOT NULL REFERENCES therapist(id) ON DELETE CASCADE,
    id_paciente INTEGER NOT NULL REFERENCES patient(id) ON DELETE CASCADE,
    mensaje TEXT,
    leido BOOLEAN DEFAULT FALSE,
    fecha_compartido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_leido TIMESTAMP
);

-- Índices
CREATE INDEX idx_video_share_captura ON video_share(id_captura);
CREATE INDEX idx_video_share_terapeuta ON video_share(id_terapeuta);
CREATE INDEX idx_video_share_paciente ON video_share(id_paciente);
CREATE INDEX idx_video_share_leido ON video_share(leido);

-- ============================================
-- COMENTARIOS DE TABLAS
-- ============================================
COMMENT ON TABLE user IS 'Usuarios del sistema con autenticación';
COMMENT ON TABLE patient IS 'Información de pacientes en rehabilitación';
COMMENT ON TABLE therapist IS 'Información de terapeutas';
COMMENT ON TABLE exercise IS 'Catálogo de ejercicios disponibles';
COMMENT ON TABLE appointment IS 'Citas programadas entre pacientes y terapeutas';
COMMENT ON TABLE system_settings IS 'Configuraciones globales del sistema';
COMMENT ON TABLE session_capture IS 'Fotos y videos capturados durante sesiones';
COMMENT ON TABLE routine IS 'Rutinas de ejercicios personalizadas';
COMMENT ON TABLE routine_exercise IS 'Ejercicios específicos dentro de cada rutina';
COMMENT ON TABLE video_share IS 'Videos compartidos entre terapeutas y pacientes';

-- ============================================
-- FIN DEL ESQUEMA
-- ============================================
