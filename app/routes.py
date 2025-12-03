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
        therapists = Therapist.query.all()
        active_therapists = sum(1 for t in therapists if t.user.is_active)
        return render_template('admin/therapists.html', 
                             active_page='therapists',
                             therapists=therapists,
                             active_therapists=active_therapists,
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

    @app.route('/admin/patients')
    @login_required
    @role_required('admin')
    def admin_patients():
        patients = Patient.query.all()
        active_patients = sum(1 for p in patients if p.user.is_active)
        in_therapy = sum(1 for p in patients if p.completed_sessions < p.total_sessions and p.user.is_active)
        return render_template('admin/patients.html', 
                             active_page='patients',
                             patients=patients,
                             active_patients=active_patients,
                             in_therapy=in_therapy,
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
    
    # ============================================================
    # 👨‍⚕️ AGREGAR TERAPEUTA
    # ============================================================
    @app.route('/admin/add-therapist', methods=['POST'])
    @login_required
    @role_required('admin')
    def add_therapist():
        """Agregar nuevo terapeuta"""
        try:
            # Obtener datos del formulario
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            specialty = request.form.get('specialty', '')
            
            # Validar que no exista el usuario
            if User.query.filter_by(username=username).first():
                flash('❌ El nombre de usuario ya existe', 'danger')
                return redirect(url_for('admin_therapists'))
            
            if User.query.filter_by(email=email).first():
                flash('❌ El email ya está registrado', 'danger')
                return redirect(url_for('admin_therapists'))
            
            # Crear usuario
            user = User(
                username=username,
                email=email,
                role='therapist',
                is_active=True
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Para obtener el user.id
            
            # Crear perfil de terapeuta
            therapist = Therapist(
                user_id=user.id,
                full_name=full_name,
                specialty=specialty,
                total_patients=0
            )
            db.session.add(therapist)
            db.session.commit()
            
            flash(f'✅ Terapeuta {full_name} creado exitosamente', 'success')
            return redirect(url_for('admin_therapists'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al crear terapeuta: {str(e)}', 'danger')
            return redirect(url_for('admin_therapists'))
    
    # ============================================================
    # 🤕 AGREGAR PACIENTE
    # ============================================================
    @app.route('/admin/add-patient', methods=['POST'])
    @login_required
    @role_required('admin')
    def add_patient():
        """Agregar nuevo paciente"""
        try:
            # Obtener datos del formulario
            full_name = request.form.get('full_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            diagnosis = request.form.get('diagnosis', '')
            total_sessions = int(request.form.get('total_sessions', 20))
            
            # Validar que no exista el usuario
            if User.query.filter_by(username=username).first():
                flash('❌ El nombre de usuario ya existe', 'danger')
                return redirect(url_for('admin_patients'))
            
            if User.query.filter_by(email=email).first():
                flash('❌ El email ya está registrado', 'danger')
                return redirect(url_for('admin_patients'))
            
            # Crear usuario
            user = User(
                username=username,
                email=email,
                role='patient',
                is_active=True
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Para obtener el user.id
            
            # Crear perfil de paciente
            patient = Patient(
                user_id=user.id,
                full_name=full_name,
                diagnosis=diagnosis,
                progress=0.0,
                total_sessions=total_sessions,
                completed_sessions=0
            )
            db.session.add(patient)
            db.session.commit()
            
            flash(f'✅ Paciente {full_name} creado exitosamente', 'success')
            return redirect(url_for('admin_patients'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al crear paciente: {str(e)}', 'danger')
            return redirect(url_for('admin_patients'))
    
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
    # 📹 RUTAS DE CAPTURA DE SESIÓN (FOTOS Y VIDEOS)
    # ============================================================
    @app.route('/api/save-snapshot', methods=['POST'])
    @login_required
    @role_required('therapist')
    def save_snapshot():
        """Guardar foto capturada de la sesión"""
        try:
            import base64
            import os
            from app.models import SessionCapture
            
            data = request.get_json()
            image_data = data.get('image')
            patient_id = data.get('patient_id')
            notes = data.get('notes', '')
            
            if not image_data:
                return jsonify({'success': False, 'message': 'No se recibió imagen'}), 400
            
            # Remover el prefijo data:image/jpeg;base64,
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decodificar base64
            image_bytes = base64.b64decode(image_data)
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'snapshot_{current_user.id}_{timestamp}.jpg'
            
            # Crear ruta completa
            upload_folder = os.path.join('static', 'uploads', 'photos')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            
            # Guardar archivo
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            
            # Obtener tamaño del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar en base de datos
            therapist = Therapist.query.filter_by(user_id=current_user.id).first()
            if therapist:
                capture = SessionCapture(
                    therapist_id=therapist.id,
                    patient_id=patient_id,
                    capture_type='photo',
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    notes=notes
                )
                db.session.add(capture)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Foto guardada correctamente',
                    'filename': filename,
                    'file_size': file_size,
                    'capture_id': capture.id
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al guardar foto: {str(e)}'}), 500
    
    @app.route('/api/save-video', methods=['POST'])
    @login_required
    @role_required('therapist')
    def save_video():
        """Guardar video grabado de la sesión"""
        try:
            import os
            from app.models import SessionCapture
            
            if 'video' not in request.files:
                return jsonify({'success': False, 'message': 'No se recibió video'}), 400
            
            video_file = request.files['video']
            patient_id = request.form.get('patient_id')
            notes = request.form.get('notes', '')
            duration = request.form.get('duration', 0)
            
            if video_file.filename == '':
                return jsonify({'success': False, 'message': 'Archivo vacío'}), 400
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'video_{current_user.id}_{timestamp}.webm'
            
            # Crear ruta completa
            upload_folder = os.path.join('static', 'uploads', 'videos')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            
            # Guardar archivo
            video_file.save(file_path)
            
            # Obtener tamaño del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar en base de datos
            therapist = Therapist.query.filter_by(user_id=current_user.id).first()
            if therapist:
                capture = SessionCapture(
                    therapist_id=therapist.id,
                    patient_id=patient_id,
                    capture_type='video',
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    duration=int(duration),
                    notes=notes
                )
                db.session.add(capture)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Video guardado correctamente',
                    'filename': filename,
                    'file_size': file_size,
                    'duration': duration,
                    'capture_id': capture.id
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al guardar video: {str(e)}'}), 500
    
    @app.route('/api/get-captures', methods=['GET'])
    @login_required
    @role_required('therapist')
    def get_captures():
        """Obtener lista de capturas del terapeuta"""
        try:
            from app.models import SessionCapture
            
            therapist = Therapist.query.filter_by(user_id=current_user.id).first()
            if not therapist:
                return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
            
            captures = SessionCapture.query.filter_by(therapist_id=therapist.id).order_by(SessionCapture.created_at.desc()).all()
            
            captures_list = []
            for capture in captures:
                captures_list.append({
                    'id': capture.id,
                    'type': capture.capture_type,
                    'filename': capture.filename,
                    'file_path': capture.file_path,
                    'file_size': capture.file_size,
                    'duration': capture.duration,
                    'notes': capture.notes,
                    'patient_id': capture.patient_id,
                    'created_at': capture.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                'success': True,
                'captures': captures_list,
                'total': len(captures_list)
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al obtener capturas: {str(e)}'}), 500

    # ============================================================
    # 📹 RUTAS DE CAPTURA PARA PACIENTES
    # ============================================================
    @app.route('/api/save-patient-snapshot', methods=['POST'])
    @login_required
    @role_required('patient')
    def save_patient_snapshot():
        """Guardar foto capturada por el paciente"""
        try:
            import base64
            import os
            from app.models import SessionCapture
            
            data = request.get_json()
            image_data = data.get('image')
            notes = data.get('notes', '')
            
            if not image_data:
                return jsonify({'success': False, 'message': 'No se recibió imagen'}), 400
            
            # Remover el prefijo data:image/jpeg;base64,
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decodificar base64
            image_bytes = base64.b64decode(image_data)
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'patient_snapshot_{current_user.id}_{timestamp}.jpg'
            
            # Crear ruta completa
            upload_folder = os.path.join('static', 'uploads', 'photos')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            
            # Guardar archivo
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            
            # Obtener tamaño del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar en base de datos
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if patient:
                capture = SessionCapture(
                    therapist_id=None,  # No hay terapeuta asociado
                    patient_id=patient.id,
                    capture_type='photo',
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    notes=notes
                )
                db.session.add(capture)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Foto guardada correctamente',
                    'filename': filename,
                    'file_size': file_size,
                    'capture_id': capture.id
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al guardar foto: {str(e)}'}), 500
    
    @app.route('/api/save-patient-video', methods=['POST'])
    @login_required
    @role_required('patient')
    def save_patient_video():
        """Guardar video grabado por el paciente"""
        try:
            import os
            from app.models import SessionCapture
            
            if 'video' not in request.files:
                return jsonify({'success': False, 'message': 'No se recibió video'}), 400
            
            video_file = request.files['video']
            notes = request.form.get('notes', '')
            duration = request.form.get('duration', 0)
            
            if video_file.filename == '':
                return jsonify({'success': False, 'message': 'Archivo vacío'}), 400
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'patient_video_{current_user.id}_{timestamp}.webm'
            
            # Crear ruta completa
            upload_folder = os.path.join('static', 'uploads', 'videos')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            
            # Guardar archivo
            video_file.save(file_path)
            
            # Obtener tamaño del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar en base de datos
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if patient:
                capture = SessionCapture(
                    therapist_id=None,  # No hay terapeuta asociado
                    patient_id=patient.id,
                    capture_type='video',
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    duration=int(duration),
                    notes=notes
                )
                db.session.add(capture)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Video guardado correctamente',
                    'filename': filename,
                    'file_size': file_size,
                    'duration': duration,
                    'capture_id': capture.id
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al guardar video: {str(e)}'}), 500
    
    @app.route('/api/get-patient-captures', methods=['GET'])
    @login_required
    @role_required('patient')
    def get_patient_captures():
        """Obtener lista de capturas del paciente"""
        try:
            from app.models import SessionCapture
            
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if not patient:
                return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
            
            captures = SessionCapture.query.filter_by(patient_id=patient.id).order_by(SessionCapture.created_at.desc()).all()
            
            captures_list = []
            for capture in captures:
                captures_list.append({
                    'id': capture.id,
                    'type': capture.capture_type,
                    'filename': capture.filename,
                    'file_path': capture.file_path,
                    'file_size': capture.file_size,
                    'duration': capture.duration,
                    'notes': capture.notes,
                    'created_at': capture.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                'success': True,
                'captures': captures_list,
                'total': len(captures_list)
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al obtener capturas: {str(e)}'}), 500

    # ============================================================
    # LOGOUT
    # ============================================================
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sesión cerrada correctamente.', 'info')
        return redirect(url_for('login'))
