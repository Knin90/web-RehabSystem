-- ============================================================================
-- SISTEMA DE REHABILITACIÓN - DDL COMPLETO
-- Base de Datos: PostgreSQL / SQLite Compatible
-- Fecha de Creación: 2025-12-08
-- ============================================================================

-- ============================================================================
-- TABLA: user
-- Descripción: Almacena información de usuarios del sistema (pacientes, terapeutas, administradores)
-- ============================================================================
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario VARCHAR(80) NOT NULL UNIQUE,
    correo_electronico VARCHAR(120) NOT NULL UNIQUE,
    contrasena_encriptada VARCHAR(128) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('paciente', 'terapeuta', 'administrador')),
    esta_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    CONSTRAINT idx_user_nombre_usuario UNIQUE (nombre_usuario),
    CONSTRAINT idx_user_correo UNIQUE (correo_electronico)
);

CREATE INDEX idx_user_rol ON user(rol);
CREATE INDEX idx_user_activo ON user(esta_activo);

-- ============================================================================
-- TABLA: patient
-- Descripción: Perfil extendido para usuarios con rol de paciente
-- ============================================================================
CREATE TABLE patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL UNIQUE,
    nombre_completo VARCHAR(200) NOT NULL,
    diagnostico TEXT,
    progreso REAL DEFAULT 0.0,
    sesiones_totales INTEGER DEFAULT 0,
    sesiones_completadas INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    FOREIGN KEY (id_usuario) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_patient_usuario ON patient(id_usuario);
CREATE INDEX idx_patient_progreso ON patient(progreso);

-- ============================================================================
-- TABLA: therapist
-- Descripción: Perfil extendido para usuarios con rol de terapeuta
-- ============================================================================
CREATE TABLE therapist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL UNIQUE,
    nombre_completo VARCHAR(200) NOT NULL,
    especialidad VARCHAR(100),
    total_pacientes INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    FOREIGN KEY (id_usuario) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_therapist_usuario ON therapist(id_usuario);
CREATE INDEX idx_therapist_especialidad ON therapist(especialidad);

-- ============================================================================
-- TABLA: exercise
-- Descripción: Catálogo de ejercicios disponibles en el sistema
-- ============================================================================
CREATE TABLE exercise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    repeticiones VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_exercise_categoria ON exercise(categoria);
CREATE INDEX idx_exercise_nombre ON exercise(nombre);

-- ============================================================================
-- TABLA: routine
-- Descripción: Rutinas de ejercicios creadas por terapeutas
-- ============================================================================
CREATE TABLE routine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    id_terapeuta INTEGER NOT NULL,
    id_paciente INTEGER,
    duracion_minutos INTEGER DEFAULT 30,
    dificultad VARCHAR(20) DEFAULT 'media' CHECK (dificultad IN ('facil', 'media', 'dificil')),
    esta_activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    FOREIGN KEY (id_terapeuta) REFERENCES therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES patient(id) ON DELETE SET NULL
);

CREATE INDEX idx_routine_terapeuta ON routine(id_terapeuta);
CREATE INDEX idx_routine_paciente ON routine(id_paciente);
CREATE INDEX idx_routine_activa ON routine(esta_activa);

-- ============================================================================
-- TABLA: routine_exercise
-- Descripción: Tabla intermedia que relaciona ejercicios con rutinas
-- ============================================================================
CREATE TABLE routine_exercise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rutina INTEGER NOT NULL,
    id_ejercicio INTEGER NOT NULL,
    orden INTEGER DEFAULT 0,
    series INTEGER DEFAULT 3,
    repeticiones INTEGER DEFAULT 10,
    segundos_descanso INTEGER DEFAULT 30,
    notas TEXT,
    
    -- Relaciones
    FOREIGN KEY (id_rutina) REFERENCES routine(id) ON DELETE CASCADE,
    FOREIGN KEY (id_ejercicio) REFERENCES exercise(id) ON DELETE CASCADE
);

CREATE INDEX idx_routine_exercise_rutina ON routine_exercise(id_rutina);
CREATE INDEX idx_routine_exercise_ejercicio ON routine_exercise(id_ejercicio);
CREATE INDEX idx_routine_exercise_orden ON routine_exercise(orden);

-- ============================================================================
-- TABLA: appointment
-- Descripción: Citas programadas entre pacientes y terapeutas
-- ============================================================================
CREATE TABLE appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER,
    id_terapeuta INTEGER,
    fecha TIMESTAMP NOT NULL,
    estado VARCHAR(20) DEFAULT 'programada' CHECK (estado IN ('programada', 'completada', 'cancelada')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    FOREIGN KEY (id_paciente) REFERENCES patient(id) ON DELETE CASCADE,
    FOREIGN KEY (id_terapeuta) REFERENCES therapist(id) ON DELETE CASCADE
);

CREATE INDEX idx_appointment_paciente ON appointment(id_paciente);
CREATE INDEX idx_appointment_terapeuta ON appointment(id_terapeuta);
CREATE INDEX idx_appointment_fecha ON appointment(fecha);
CREATE INDEX idx_appointment_estado ON appointment(estado);

-- ============================================================================
-- TABLA: session_capture
-- Descripción: Almacena fotos y videos capturados durante las sesiones
-- ============================================================================
CREATE TABLE session_capture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_terapeuta INTEGER,
    id_paciente INTEGER,
    tipo_captura VARCHAR(20) NOT NULL CHECK (tipo_captura IN ('photo', 'video')),
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tamano_archivo INTEGER,
    duracion INTEGER,
    notas TEXT,
    fecha_sesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    es_permanente BOOLEAN DEFAULT FALSE,
    contiene_audio BOOLEAN DEFAULT FALSE,
    
    -- Relaciones
    FOREIGN KEY (id_terapeuta) REFERENCES therapist(id) ON DELETE SET NULL,
    FOREIGN KEY (id_paciente) REFERENCES patient(id) ON DELETE SET NULL
);

CREATE INDEX idx_session_capture_terapeuta ON session_capture(id_terapeuta);
CREATE INDEX idx_session_capture_paciente ON session_capture(id_paciente);
CREATE INDEX idx_session_capture_tipo ON session_capture(tipo_captura);
CREATE INDEX idx_session_capture_fecha ON session_capture(fecha_sesion);

-- ============================================================================
-- TABLA: video_share
-- Descripción: Gestiona el compartir videos entre terapeutas y pacientes
-- ============================================================================
CREATE TABLE video_share (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura INTEGER NOT NULL,
    id_terapeuta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    mensaje TEXT,
    leido BOOLEAN DEFAULT FALSE,
    fecha_compartido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_leido TIMESTAMP,
    
    -- Relaciones
    FOREIGN KEY (id_captura) REFERENCES session_capture(id) ON DELETE CASCADE,
    FOREIGN KEY (id_terapeuta) REFERENCES therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES patient(id) ON DELETE CASCADE
);

CREATE INDEX idx_video_share_captura ON video_share(id_captura);
CREATE INDEX idx_video_share_terapeuta ON video_share(id_terapeuta);
CREATE INDEX idx_video_share_paciente ON video_share(id_paciente);
CREATE INDEX idx_video_share_leido ON video_share(leido);

-- ============================================================================
-- TABLA: system_settings
-- Descripción: Configuraciones del sistema (clave-valor)
-- ============================================================================
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor VARCHAR(500),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT idx_system_settings_clave UNIQUE (clave)
);

CREATE INDEX idx_system_settings_clave_idx ON system_settings(clave);

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================

-- Configuraciones del sistema
INSERT INTO system_settings (clave, valor) VALUES 
    ('sistema_nombre', 'Sistema de Rehabilitación'),
    ('version', '1.0.0'),
    ('mantenimiento', 'false'),
    ('max_upload_size', '524288000');

-- Ejercicios de ejemplo
INSERT INTO exercise (nombre, descripcion, categoria, repeticiones) VALUES
    ('Flexión de rodilla', 'Ejercicio para fortalecer cuádriceps', 'Piernas', '3 series de 10'),
    ('Extensión de brazo', 'Ejercicio para fortalecer bíceps y tríceps', 'Brazos', '3 series de 12'),
    ('Rotación de hombro', 'Ejercicio para movilidad del hombro', 'Hombros', '2 series de 15'),
    ('Estiramiento lumbar', 'Ejercicio para flexibilidad de espalda baja', 'Espalda', '3 repeticiones de 30 segundos'),
    ('Elevación de talones', 'Ejercicio para fortalecer pantorrillas', 'Piernas', '3 series de 15');

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Resumen de pacientes con su información de usuario
CREATE VIEW vista_pacientes_completo AS
SELECT 
    p.id,
    p.nombre_completo,
    p.diagnostico,
    p.progreso,
    p.sesiones_totales,
    p.sesiones_completadas,
    u.nombre_usuario,
    u.correo_electronico,
    u.esta_activo,
    p.fecha_creacion
FROM patient p
INNER JOIN user u ON p.id_usuario = u.id;

-- Vista: Resumen de terapeutas con su información de usuario
CREATE VIEW vista_terapeutas_completo AS
SELECT 
    t.id,
    t.nombre_completo,
    t.especialidad,
    t.total_pacientes,
    u.nombre_usuario,
    u.correo_electronico,
    u.esta_activo,
    t.fecha_creacion
FROM therapist t
INNER JOIN user u ON t.id_usuario = u.id;

-- Vista: Rutinas con información del terapeuta y paciente
CREATE VIEW vista_rutinas_detalle AS
SELECT 
    r.id,
    r.nombre,
    r.descripcion,
    r.duracion_minutos,
    r.dificultad,
    r.esta_activa,
    t.nombre_completo AS terapeuta_nombre,
    p.nombre_completo AS paciente_nombre,
    r.fecha_creacion
FROM routine r
INNER JOIN therapist t ON r.id_terapeuta = t.id
LEFT JOIN patient p ON r.id_paciente = p.id;

-- Vista: Citas con información completa
CREATE VIEW vista_citas_completo AS
SELECT 
    a.id,
    a.fecha,
    a.estado,
    p.nombre_completo AS paciente_nombre,
    t.nombre_completo AS terapeuta_nombre,
    a.fecha_creacion
FROM appointment a
LEFT JOIN patient p ON a.id_paciente = p.id
LEFT JOIN therapist t ON a.id_terapeuta = t.id;

-- ============================================================================
-- FIN DEL SCRIPT DDL
-- ============================================================================
