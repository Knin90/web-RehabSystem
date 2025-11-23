from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Patient, Therapist, Exercise
from app.forms import LoginForm

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('No tienes permisos.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/seleccionar-modulo')
    def select_module():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('seleccionar_modulo.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        modulo = request.args.get('modulo', '')
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and user.check_password(form.password.data):
                if modulo and user.role != modulo:
                    flash('No tienes permisos para este módulo.', 'error')
                    return render_template('login.html', form=form, modulo_seleccionado=modulo)
                
                login_user(user)
                flash(f'¡Bienvenido/a {user.username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales incorrectas.', 'error')
        
        return render_template('login.html', form=form, modulo_seleccionado=modulo)
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
        elif current_user.role == 'therapist':
            return redirect(url_for('therapist_dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('index'))
    
    @app.route('/patient/dashboard')
    @login_required
    @role_required('patient')
    def patient_dashboard():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            patient = Patient(user_id=current_user.id, full_name=current_user.username)
            db.session.add(patient)
            db.session.commit()
        
        datos = {
            'nombre_completo': patient.full_name,
            'diagnostico': patient.diagnosis or 'Sin diagnóstico',
            'progreso': patient.progress,
            'sesiones_completadas': patient.completed_sessions,
            'sesiones_totales': patient.total_sessions,
            'citas_proximas': [],
            'ejercicios_asignados': [],
            'terapeutas': [],
            'recordatorios': []
        }
        return render_template('dashboard_paciente.html', 
                             usuario={'username': current_user.username, 'rol': 'paciente'},
                             datos=datos)
    
    @app.route('/therapist/dashboard')
    @login_required
    @role_required('therapist')
    def therapist_dashboard():
        therapist = Therapist.query.filter_by(user_id=current_user.id).first()
        if not therapist:
            therapist = Therapist(user_id=current_user.id, full_name=current_user.username)
            db.session.add(therapist)
            db.session.commit()
        
        datos = {
            'nombre_completo': therapist.full_name,
            'especialidad': therapist.specialty or 'Fisioterapeuta',
            'email': current_user.email,
            'pacientes_total': therapist.total_patients,
            'citas_proximas': [],
            'mensajes': []
        }
        return render_template('dashboard_terapeuta.html',
                             usuario={'username': current_user.username, 'rol': 'terapeuta'},
                             datos=datos)
    
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        datos = {
            'nombre_completo': 'Administrador',
            'email': current_user.email,
            'estadisticas': {
                'usuarios_totales': User.query.count(),
                'terapeutas_activos': Therapist.query.count(),
                'pacientes_activos': Patient.query.count(),
                'citas_hoy': 0
            }
        }
        return render_template('dashboard_admin.html',
                             usuario={'username': current_user.username, 'rol': 'admin'},
                             datos=datos)
    
    @app.route('/logout')
    @login_required
    def logout():
        nombre = current_user.username
        logout_user()
        flash(f'¡Hasta pronto, {nombre}!', 'info')
        return redirect(url_for('index', from_logout='true'))
    
    
    @app.route('/api/patients', methods=['GET'])
    @login_required
    def api_patients():
        from flask import jsonify
        patients = Patient.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.full_name,
            'progress': p.progress
        } for p in patients])
    
    @app.route('/api/exercises', methods=['GET'])
    @login_required
    def api_exercises():
        from flask import jsonify
        exercises = Exercise.query.all()
        return jsonify([{
            'id': e.id,
            'name': e.name,
            'category': e.category
        } for e in exercises])