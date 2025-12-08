from datetime import datetime
from app import db, bcrypt, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_encriptada = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    esta_activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    perfil_paciente = db.relationship('Patient', backref='usuario', uselist=False)
    perfil_terapeuta = db.relationship('Therapist', backref='usuario', uselist=False)
    
    def set_password(self, password):
        self.contrasena_encriptada = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.contrasena_encriptada, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    diagnostico = db.Column(db.Text)
    progreso = db.Column(db.Float, default=0.0)
    sesiones_totales = db.Column(db.Integer, default=0)
    sesiones_completadas = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con rutinas asignadas
    rutinas_asignadas = db.relationship('Routine', foreign_keys='Routine.id_paciente', backref='paciente_asignado', lazy='dynamic')

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    especialidad = db.Column(db.String(100))
    total_pacientes = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def pacientes_asignados(self):
        """Obtener pacientes únicos asignados a través de rutinas"""
        # Importar aquí para evitar referencias circulares
        rutinas = db.session.query(Routine).filter_by(id_terapeuta=self.id).filter(Routine.id_paciente.isnot(None)).all()
        pacientes_ids = list(set([r.id_paciente for r in rutinas]))
        return db.session.query(Patient).filter(Patient.id.in_(pacientes_ids)).all() if pacientes_ids else []

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    repeticiones = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('patient.id'))
    id_terapeuta = db.Column(db.Integer, db.ForeignKey('therapist.id'))
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default='programada')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.String(500))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_setting(clave, valor_predeterminado=None):
        configuracion = SystemSettings.query.filter_by(clave=clave).first()
        return configuracion.valor if configuracion else valor_predeterminado
    
    @staticmethod
    def set_setting(clave, valor):
        configuracion = SystemSettings.query.filter_by(clave=clave).first()
        if configuracion:
            configuracion.valor = valor
            configuracion.fecha_actualizacion = datetime.utcnow()
        else:
            configuracion = SystemSettings(clave=clave, valor=valor)
            db.session.add(configuracion)
        db.session.commit()
        return configuracion

class SessionCapture(db.Model):
    """Modelo para almacenar capturas de fotos y videos de sesiones"""
    id = db.Column(db.Integer, primary_key=True)
    id_terapeuta = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=True)  # Nullable para capturas de pacientes
    id_paciente = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    tipo_captura = db.Column(db.String(20), nullable=False)  # 'photo' o 'video'
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    tamano_archivo = db.Column(db.Integer)  # Tamaño en bytes
    duracion = db.Column(db.Integer)  # Duración en segundos (solo para videos)
    notas = db.Column(db.Text)  # Notas del terapeuta o paciente
    fecha_sesion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    es_permanente = db.Column(db.Boolean, default=False)  # Nuevo campo para grabaciones permanentes
    contiene_audio = db.Column(db.Boolean, default=False)  # Nuevo campo para indicar si tiene audio
    
    # Relaciones
    terapeuta = db.relationship('Therapist', backref='capturas')
    paciente = db.relationship('Patient', backref='capturas')

class Routine(db.Model):
    """Modelo para rutinas de ejercicios"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    id_terapeuta = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)  # Null = rutina template
    duracion_minutos = db.Column(db.Integer, default=30)
    dificultad = db.Column(db.String(20), default='media')  # facil, media, dificil
    esta_activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    terapeuta = db.relationship('Therapist', backref='rutinas_creadas')
    paciente = db.relationship('Patient', backref='rutinas', overlaps="paciente_asignado,rutinas_asignadas")
    ejercicios = db.relationship('RoutineExercise', backref='rutina', cascade='all, delete-orphan')

class RoutineExercise(db.Model):
    """Tabla intermedia para ejercicios en rutinas"""
    id = db.Column(db.Integer, primary_key=True)
    id_rutina = db.Column(db.Integer, db.ForeignKey('routine.id'), nullable=False)
    id_ejercicio = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    orden = db.Column(db.Integer, default=0)  # Orden en la rutina
    series = db.Column(db.Integer, default=3)
    repeticiones = db.Column(db.Integer, default=10)
    segundos_descanso = db.Column(db.Integer, default=30)
    notas = db.Column(db.Text)
    
    # Relaciones
    ejercicio = db.relationship('Exercise', backref='ejercicios_rutina')

class VideoShare(db.Model):
    """Modelo para compartir videos entre terapeuta y paciente"""
    id = db.Column(db.Integer, primary_key=True)
    id_captura = db.Column(db.Integer, db.ForeignKey('session_capture.id'), nullable=False)
    id_terapeuta = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    mensaje = db.Column(db.Text)  # Mensaje del terapeuta al paciente
    leido = db.Column(db.Boolean, default=False)  # Si el paciente ha visto el video
    fecha_compartido = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_leido = db.Column(db.DateTime)  # Cuándo el paciente vio el video
    
    # Relaciones
    captura = db.relationship('SessionCapture', backref='compartidos')
    terapeuta = db.relationship('Therapist', backref='videos_compartidos')
    paciente = db.relationship('Patient', backref='videos_recibidos')