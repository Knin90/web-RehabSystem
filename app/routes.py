from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Patient, Therapist, Exercise, Appointment, SystemSettings
from app.forms import LoginForm
import csv
import io
from datetime import datetime


# ============================================================
# 🔐 Decorador para roles
# ============================================================
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('No tienes permisos para acceder a esta sección.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============================================================
# 🔗 Registrar rutas
# ============================================================
def register_routes(app):

    # --------------------------------------------------------
    # Página principal
    # --------------------------------------------------------
    @app.route('/')
    def index():
        return render_template('index.html')

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and user.check_password(form.password.data):
                login_user(user)

                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'therapist':
                    return redirect(url_for('therapist_dashboard'))
                elif user.role == 'patient':
                    return redirect(url_for('patient_dashboard'))

                flash("Tu rol no está configurado correctamente.", "danger")
                return redirect(url_for('login'))

            flash('Credenciales incorrectas.', 'danger')

        return render_template('login.html', form=form)

    # ============================================================
    # 👤 PÁGINAS DEL PACIENTE
    # ============================================================
    def obtener_datos_paciente():
        patient = Patient.query.filter_by(user_id=current_user.id).first()

        if not patient:
            patient = Patient(user_id=current_user.id, full_name=current_user.username)
            db.session.add(patient)
            db.session.commit()

        return {
            'nombre_completo': patient.full_name,
            'diagnostico': patient.diagnosis or 'Sin diagnóstico',
            'progreso': patient.progress,
            'sesiones_completadas': patient.completed_sessions,
            'sesiones_totales': patient.total_sessions
        }

    @app.route('/patient/dashboard')
    @login_required
    @role_required('patient')
    def patient_dashboard():
        return render_template('patient/dashboard.html', datos=obtener_datos_paciente(), active_page='dashboard')

    @app.route('/patient/history')
    @login_required
    @role_required('patient')
    def patient_history():
        return render_template('patient/history.html', datos=obtener_datos_paciente(), active_page='history')

    @app.route('/patient/therapists')
    @login_required
    @role_required('patient')
    def patient_therapists():
        return render_template('patient/therapists.html', datos=obtener_datos_paciente(), active_page='therapists')

    @app.route('/patient/start-therapy')
    @login_required
    @role_required('patient')
    def patient_start_therapy():
        return render_template('patient/start_therapy.html', datos=obtener_datos_paciente(), active_page='start_therapy')

    @app.route('/patient/messages')
    @login_required
    @role_required('patient')
    def patient_messages():
        return render_template('patient/messages.html', datos=obtener_datos_paciente(), active_page='messages')

    @app.route('/patient/settings')
    @login_required
    @role_required('patient')
    def patient_settings():
        return render_template('patient/settings.html', datos=obtener_datos_paciente(), active_page='settings')

    @app.route('/patient/profile')
    @login_required
    @role_required('patient')
    def patient_profile():
        return render_template('patient/profile.html', datos=obtener_datos_paciente(), active_page='profile')

    # ============================================================
    # 🧑‍⚕️ PÁGINAS DEL TERAPEUTA
    # ============================================================
    @app.route('/therapist/dashboard')
    @login_required
    @role_required('therapist')
    def therapist_dashboard():
        return render_template('therapist/dashboard.html', active_page='dashboard')

    @app.route('/therapist/patients')
    @login_required
    @role_required('therapist')
    def therapist_patients():
        return render_template('therapist/patients.html', active_page='patients')

    @app.route('/therapist/start-session')
    @login_required
    @role_required('therapist')
    def therapist_start_session():
        return render_template('therapist/start_session.html', active_page='start_session')

    @app.route('/therapist/appointments')
    @login_required
    @role_required('therapist')
    def therapist_appointments():
        return render_template('therapist/appointments.html', active_page='appointments')

    @app.route('/therapist/routines')
    @login_required
    @role_required('therapist')
    def therapist_routines():
        return render_template('therapist/routines.html', active_page='routines')

    # ============================================================
    # 🛠️ PÁGINAS DEL ADMINISTRADOR
    # ============================================================
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        return render_template('admin/dashboard.html', active_page='dashboard',
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

    @app.route('/admin/users')
    @login_required
    @role_required('admin')
    def admin_users():
        return render_template('admin/users.html', active_page='users',
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

    @app.route('/admin/therapists')
    @login_required
    @role_required('admin')
    def admin_therapists():
        return render_template('admin/therapists.html', active_page='therapists',
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

    @app.route('/admin/patients')
    @login_required
    @role_required('admin')
    def admin_patients():
        return render_template('admin/patients.html', active_page='patients',
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

    @app.route('/admin/settings', methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def admin_settings():
        if request.method == 'POST':
            setting_type = request.form.get('setting_type')
            
            if setting_type == 'session_duration':
                SystemSettings.set_setting('session_duration', request.form.get('session_duration', '45'))
                SystemSettings.set_setting('sessions_per_week', request.form.get('sessions_per_week', '3'))
                SystemSettings.set_setting('rest_time', request.form.get('rest_time', '30'))
                flash('✅ Duración de sesión actualizada correctamente.', 'success')
                
            elif setting_type == 'notifications':
                SystemSettings.set_setting('email_notifications', request.form.get('email_notifications', 'off'))
                SystemSettings.set_setting('appointment_reminder', request.form.get('appointment_reminder', 'off'))
                SystemSettings.set_setting('progress_report', request.form.get('progress_report', 'off'))
                SystemSettings.set_setting('inactive_alert', request.form.get('inactive_alert', 'off'))
                flash('✅ Configuración de notificaciones actualizada.', 'success')
                
            elif setting_type == 'backup':
                SystemSettings.set_setting('auto_backup', request.form.get('auto_backup', 'off'))
                SystemSettings.set_setting('backup_time', request.form.get('backup_time', '02:00'))
                SystemSettings.set_setting('backup_retention', request.form.get('backup_retention', '30'))
                SystemSettings.set_setting('auto_cleanup', request.form.get('auto_cleanup', 'off'))
                flash('✅ Respaldo automático configurado.', 'success')
                
            elif setting_type == 'security':
                SystemSettings.set_setting('session_timeout', request.form.get('session_timeout', '60'))
                SystemSettings.set_setting('two_factor', request.form.get('two_factor', 'off'))
                SystemSettings.set_setting('password_expiry', request.form.get('password_expiry', 'off'))
                SystemSettings.set_setting('max_login_attempts', request.form.get('max_login_attempts', '5'))
                flash('✅ Configuración de seguridad actualizada.', 'success')
                
            elif setting_type == 'ai_vision':
                SystemSettings.set_setting('detection_accuracy', request.form.get('detection_accuracy', '85'))
                SystemSettings.set_setting('realtime_analysis', request.form.get('realtime_analysis', 'off'))
                SystemSettings.set_setting('posture_correction', request.form.get('posture_correction', 'off'))
                SystemSettings.set_setting('capture_fps', request.form.get('capture_fps', '30'))
                flash('✅ Configuración de visión artificial actualizada.', 'success')
                
            elif setting_type == 'appearance':
                theme = request.form.get('theme', 'light')
                language = request.form.get('language', 'es')
                compact_mode = request.form.get('compact_mode', 'off')
                
                SystemSettings.set_setting('theme', theme)
                SystemSettings.set_setting('language', language)
                SystemSettings.set_setting('compact_mode', compact_mode)
                
                flash(f'✅ Tema cambiado a "{theme}" e idioma a "{language}".', 'success')
            
            return redirect(url_for('admin_settings'))
        
        # Cargar configuraciones actuales
        settings = {
            'session_duration': SystemSettings.get_setting('session_duration', '45'),
            'sessions_per_week': SystemSettings.get_setting('sessions_per_week', '3'),
            'rest_time': SystemSettings.get_setting('rest_time', '30'),
            'email_notifications': SystemSettings.get_setting('email_notifications', 'on'),
            'appointment_reminder': SystemSettings.get_setting('appointment_reminder', 'on'),
            'progress_report': SystemSettings.get_setting('progress_report', 'on'),
            'inactive_alert': SystemSettings.get_setting('inactive_alert', 'off'),
            'session_timeout': SystemSettings.get_setting('session_timeout', '60'),
            'two_factor': SystemSettings.get_setting('two_factor', 'off'),
            'password_expiry': SystemSettings.get_setting('password_expiry', 'off'),
            'max_login_attempts': SystemSettings.get_setting('max_login_attempts', '5'),
            'auto_backup': SystemSettings.get_setting('auto_backup', 'on'),
            'backup_time': SystemSettings.get_setting('backup_time', '02:00'),
            'backup_retention': SystemSettings.get_setting('backup_retention', '30'),
            'auto_cleanup': SystemSettings.get_setting('auto_cleanup', 'off'),
            'detection_accuracy': SystemSettings.get_setting('detection_accuracy', '85'),
            'realtime_analysis': SystemSettings.get_setting('realtime_analysis', 'on'),
            'posture_correction': SystemSettings.get_setting('posture_correction', 'on'),
            'capture_fps': SystemSettings.get_setting('capture_fps', '30'),
            'theme': SystemSettings.get_setting('theme', 'light'),
            'language': SystemSettings.get_setting('language', 'es'),
            'compact_mode': SystemSettings.get_setting('compact_mode', 'off')
        }
        
        return render_template('admin/settings.html', active_page='settings', settings=settings,
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))
    
    @app.route('/admin/export-data')
    @login_required
    @role_required('admin')
    def admin_export_data():
        stats = {
            'total_users': User.query.count(),
            'total_patients': Patient.query.count(),
            'total_therapists': Therapist.query.count(),
            'total_exercises': Exercise.query.count()
        }
        return render_template('admin/export_data.html', active_page='export', **stats,
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))
    
    @app.route('/admin/export/<data_type>')
    @login_required
    @role_required('admin')
    def admin_export(data_type):
        output = io.StringIO()
        writer = csv.writer(output)
        
        if data_type == 'users':
            writer.writerow(['ID', 'Usuario', 'Email', 'Rol', 'Activo', 'Fecha Creación'])
            users = User.query.all()
            for user in users:
                writer.writerow([
                    user.id, user.username, user.email, user.role, 
                    'Sí' if user.is_active else 'No', 
                    user.created_at.strftime('%Y-%m-%d %H:%M')
                ])
            filename = f'usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'patients':
            writer.writerow(['ID', 'Nombre', 'Diagnóstico', 'Progreso', 'Sesiones Completadas', 'Sesiones Totales', 'Fecha Creación'])
            patients = Patient.query.all()
            for patient in patients:
                writer.writerow([
                    patient.id, patient.full_name, patient.diagnosis or 'N/A', 
                    f'{patient.progress}%', patient.completed_sessions, 
                    patient.total_sessions, patient.created_at.strftime('%Y-%m-%d')
                ])
            filename = f'pacientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'therapists':
            writer.writerow(['ID', 'Nombre', 'Especialidad', 'Total Pacientes', 'Fecha Creación'])
            therapists = Therapist.query.all()
            for therapist in therapists:
                writer.writerow([
                    therapist.id, therapist.full_name, therapist.specialty or 'N/A',
                    therapist.total_patients, therapist.created_at.strftime('%Y-%m-%d')
                ])
            filename = f'terapeutas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'exercises':
            writer.writerow(['ID', 'Nombre', 'Descripción', 'Categoría', 'Repeticiones', 'Fecha Creación'])
            exercises = Exercise.query.all()
            for exercise in exercises:
                writer.writerow([
                    exercise.id, exercise.name, exercise.description or 'N/A',
                    exercise.category or 'N/A', exercise.repetitions or 'N/A',
                    exercise.created_at.strftime('%Y-%m-%d')
                ])
            filename = f'ejercicios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'all':
            # Exportar todo en un archivo completo
            writer.writerow(['=== USUARIOS ==='])
            writer.writerow(['ID', 'Usuario', 'Email', 'Rol', 'Activo'])
            for user in User.query.all():
                writer.writerow([user.id, user.username, user.email, user.role, 'Sí' if user.is_active else 'No'])
            
            writer.writerow([])
            writer.writerow(['=== PACIENTES ==='])
            writer.writerow(['ID', 'Nombre', 'Diagnóstico', 'Progreso', 'Sesiones'])
            for patient in Patient.query.all():
                writer.writerow([patient.id, patient.full_name, patient.diagnosis or 'N/A', f'{patient.progress}%', f'{patient.completed_sessions}/{patient.total_sessions}'])
            
            writer.writerow([])
            writer.writerow(['=== TERAPEUTAS ==='])
            writer.writerow(['ID', 'Nombre', 'Especialidad', 'Total Pacientes'])
            for therapist in Therapist.query.all():
                writer.writerow([therapist.id, therapist.full_name, therapist.specialty or 'N/A', therapist.total_patients])
            
            writer.writerow([])
            writer.writerow(['=== EJERCICIOS ==='])
            writer.writerow(['ID', 'Nombre', 'Categoría', 'Repeticiones'])
            for exercise in Exercise.query.all():
                writer.writerow([exercise.id, exercise.name, exercise.category or 'N/A', exercise.repetitions or 'N/A'])
            
            filename = f'rehabsystem_completo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        else:
            flash('Tipo de exportación no válido.', 'danger')
            return redirect(url_for('admin_export_data'))
        
        # Crear respuesta con el archivo CSV
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )

    # ============================================================
    # DASHBOARD GENERAL
    # ============================================================
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'therapist':
            return redirect(url_for('therapist_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
        return redirect(url_for('index'))

    # ============================================================
    # LOGOUT
    # ============================================================
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sesión cerrada correctamente.', 'info')
        return redirect(url_for('login'))
