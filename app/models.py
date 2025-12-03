from datetime import datetime
from app import db, bcrypt, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient_profile = db.relationship('Patient', backref='user', uselist=False)
    therapist_profile = db.relationship('Therapist', backref='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    full_name = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.Text)
    progress = db.Column(db.Float, default=0.0)
    total_sessions = db.Column(db.Integer, default=0)
    completed_sessions = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    full_name = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(100))
    total_patients = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    repetitions = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'))
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_setting(key, default=None):
        setting = SystemSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_setting(key, value):
        setting = SystemSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = SystemSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return setting

class SessionCapture(db.Model):
    """Modelo para almacenar capturas de fotos y videos de sesiones"""
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=True)  # Nullable para capturas de pacientes
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    capture_type = db.Column(db.String(20), nullable=False)  # 'photo' o 'video'
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # Tamaño en bytes
    duration = db.Column(db.Integer)  # Duración en segundos (solo para videos)
    notes = db.Column(db.Text)  # Notas del terapeuta o paciente
    session_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    therapist = db.relationship('Therapist', backref='captures')
    patient = db.relationship('Patient', backref='captures')

class Routine(db.Model):
    """Modelo para rutinas de ejercicios"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)  # Null = rutina template
    duration_minutes = db.Column(db.Integer, default=30)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    therapist = db.relationship('Therapist', backref='routines')
    patient = db.relationship('Patient', backref='routines')
    exercises = db.relationship('RoutineExercise', backref='routine', cascade='all, delete-orphan')

class RoutineExercise(db.Model):
    """Tabla intermedia para ejercicios en rutinas"""
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    order = db.Column(db.Integer, default=0)  # Orden en la rutina
    sets = db.Column(db.Integer, default=3)
    repetitions = db.Column(db.Integer, default=10)
    rest_seconds = db.Column(db.Integer, default=30)
    notes = db.Column(db.Text)
    
    # Relaciones
    exercise = db.relationship('Exercise', backref='routine_exercises')