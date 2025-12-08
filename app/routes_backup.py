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
            if not current_user.is_authenticated or current_user.rol != role:
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
            user = User.query.filter_by(nombre_usuario=form.nombre_usuario.data).first()

            if user and user.check_password(form.contrasena.data):
                login_user(user)

                if user.rol == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.rol == 'therapist':
                    return redirect(url_for('therapist_dashboard'))
                elif user.rol == 'patient':
                    return redirect(url_for('patient_dashboard'))

                flash("Tu rol no está configurado correctamente.", "danger")
                return redirect(url_for('login'))

            flash('Credenciales incorrectas.', 'danger')

            return render_template('login.html', form=form)

# ============================================================
    # 👤 PÁGINAS DEL PACIENTE
    # ============================================================
def obtener_datos_paciente():
        paciente = Patient.query.filter_by(id_usuario=current_user.id).first()

        if not paciente:
            paciente = Patient(id_usuario=current_user.id, nombre_completo=current_user.nombre_usuario)
            db.session.add(paciente)
            db.session.commit()

        return {
            'nombre_completo': paciente.nombre_completo,
            'diagnostico': paciente.diagnostico or 'Sin diagnóstico',
            'progreso': paciente.progreso,
            'sesiones_completadas': paciente.sesiones_completadas,
            'sesiones_totales': paciente.sesiones_totales
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

        @app.route('/patient/video-gallery')
        @login_required
        @role_required('patient')
        def patient_video_gallery():
                return render_template('patient/video_gallery.html', datos=obtener_datos_paciente(), active_page='video_gallery')

        @app.route('/patient/routines')
        @login_required
        @role_required('patient')
        def patient_routines():
            """Ver rutinas asignadas al paciente"""
try:
            from app.models import Routine
        
        paciente = Patient.query.filter_by(id_usuario=current_user.id).first()
        if not paciente:
            paciente = Patient(id_usuario=current_user.id, nombre_completo=current_user.nombre_usuario)
            db.session.add(paciente)
            db.session.commit()
        
        # Obtener rutinas asignadas a este paciente
        rutinas = Routine.query.filter_by(id_paciente=paciente.id).all()
        
        return render_template('patient/routines.html', 
                             datos=obtener_datos_paciente(),
                             active_page='routines',
                             routines=rutinas)
        except Exception as e:
            print(f"Error en patient_routines: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f"Error al cargar rutinas: {str(e)}", 'danger')
            return redirect(url_for('patient_dashboard'))

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
        try:
            from app.models import Routine
            terapeuta = Therapist.query.filter_by(id_usuario=current_user.id).first()
            
            # Si no existe el perfil de terapeuta, crearlo
            if not terapeuta:
                terapeuta = Therapist(
                    id_usuario=current_user.id,
                    nombre_completo=current_user.nombre_usuario,
                    especialidad='General',
                    total_pacientes=0
                )
                db.session.add(terapeuta)
                db.session.commit()
            
            rutinas = Routine.query.filter_by(id_terapeuta=terapeuta.id).all()
            ejercicios = Exercise.query.all()
            pacientes = Patient.query.join(User).filter(User.esta_activo == True).all()
            
            return render_template('therapist/routines.html', 
                                 active_page='routines',
                                 routines=rutinas,
                                 exercises=ejercicios,
                                 patients=pacientes)
        except Exception as e:
            print(f"Error en therapist_routines: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Error al cargar rutinas: {str(e)}', 'danger')
            return redirect(url_for('therapist_dashboard'))

    @app.route('/therapist/video-gallery')
    @login_required
    @role_required('therapist')
    def therapist_video_gallery():
        return render_template('therapist/video_gallery.html', active_page='video_gallery')

    # ============================================================
    # 📋 GESTIÓN DE RUTINAS (TERAPEUTA)
    # ============================================================
    @app.route('/therapist/create-routine', methods=['POST'])
    @login_required
    @role_required('therapist')
    def create_routine():
        """Crear nueva rutina"""
        try:
            from app.models import Routine, RoutineExercise
            import json
            
            terapeuta = Therapist.query.filter_by(id_usuario=current_user.id).first()
            if not terapeuta:
                return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
            
            datos = request.get_json()
            nombre = datos.get('name')
            descripcion = datos.get('description', '')
            duracion = datos.get('duration', 30)
            dificultad = datos.get('difficulty', 'media')
            ejercicios_datos = datos.get('exercises', [])
            
            # Crear rutina
            rutina = Routine(
                nombre=nombre,
                descripcion=descripcion,
                id_terapeuta=terapeuta.id,
                duracion_minutos=duracion,
                dificultad=dificultad
            )
            db.session.add(rutina)
            db.session.flush()
            
            # Agregar ejercicios a la rutina
            for idx, ex_data in enumerate(ejercicios_datos):
                ejercicio_rutina = RoutineExercise(
                    id_rutina=rutina.id,
                    id_ejercicio=ex_data['id'],
                    orden=idx,
                    series=ex_data.get('sets', 3),
                    repeticiones=ex_data.get('repetitions', 10),
                    segundos_descanso=ex_data.get('rest', 30)
                )
                db.session.add(ejercicio_rutina)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Rutina "{nombre}" creada exitosamente',
                'routine_id': rutina.id
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    @app.route('/therapist/assign-routine', methods=['POST'])
    @login_required
    @role_required('therapist')
    def assign_routine():
        """Asignar rutina a paciente"""
        try:
            from app.models import Routine, RoutineExercise
            
            datos = request.get_json()
            id_rutina = datos.get('routine_id')
            id_paciente = datos.get('patient_id')
            
            # Obtener rutina original
            rutina_original = Routine.query.get(id_rutina)
            if not rutina_original:
                return jsonify({'success': False, 'message': 'Rutina no encontrada'}), 404
            
            # Crear copia de la rutina para el paciente
            nueva_rutina = Routine(
                nombre=rutina_original.nombre,
                descripcion=rutina_original.descripcion,
                id_terapeuta=rutina_original.id_terapeuta,
                id_paciente=id_paciente,
                duracion_minutos=rutina_original.duracion_minutos,
                dificultad=rutina_original.dificultad
            )
            db.session.add(nueva_rutina)
            db.session.flush()
            
            # Copiar ejercicios
            for ex in rutina_original.ejercicios:
                nuevo_ejercicio = RoutineExercise(
                    id_rutina=nueva_rutina.id,
                    id_ejercicio=ex.id_ejercicio,
                    orden=ex.orden,
                    series=ex.series,
                    repeticiones=ex.repeticiones,
                    segundos_descanso=ex.segundos_descanso,
                    notas=ex.notas
                )
                db.session.add(nuevo_ejercicio)
            
            db.session.commit()
            
            paciente = Patient.query.get(id_paciente)
            return jsonify({
                'success': True,
                'message': f'Rutina asignada a {paciente.nombre_completo}',
                'routine_id': nueva_rutina.id
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

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
user.id, user.nombre_usuario, user.correo_electronico, user.rol, 
                    'Sí' if user.esta_activo else 'No', 
                    user.fecha_creacion.strftime('%Y-%m-%d %H:%M')
                ])
            filename = f'usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'patients':
            writer.writerow(['ID', 'Nombre', 'Diagnóstico', 'Progreso', 'Sesiones Completadas', 'Sesiones Totales', 'Fecha Creación'])
            patients = Patient.query.all()
            for patient in patients:
                writer.writerow([
patient.id, patient.nombre_completo, patient.diagnostico or 'N/A', 
                    f'{patient.progreso}%', patient.sesiones_completadas, 
                    patient.sesiones_totales, patient.fecha_creacion.strftime('%Y-%m-%d')
                ])
            filename = f'pacientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'therapists':
            writer.writerow(['ID', 'Nombre', 'Especialidad', 'Total Pacientes', 'Fecha Creación'])
            therapists = Therapist.query.all()
            for therapist in therapists:
                writer.writerow([
therapist.id, therapist.nombre_completo, therapist.especialidad or 'N/A',
                    therapist.total_pacientes, therapist.fecha_creacion.strftime('%Y-%m-%d')
                ])
            filename = f'terapeutas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'exercises':
            writer.writerow(['ID', 'Nombre', 'Descripción', 'Categoría', 'Repeticiones', 'Fecha Creación'])
            exercises = Exercise.query.all()
            for exercise in exercises:
                writer.writerow([
exercise.id, exercise.nombre, exercise.descripcion or 'N/A',
                    exercise.categoria or 'N/A', exercise.repeticiones or 'N/A',
                    exercise.fecha_creacion.strftime('%Y-%m-%d')
                ])
            filename = f'ejercicios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        elif data_type == 'all':
            # Exportar todo en un archivo completo
            writer.writerow(['=== USUARIOS ==='])
            writer.writerow(['ID', 'Usuario', 'Email', 'Rol', 'Activo'])
            for user in User.query.all():
                writer.writerow([user.id, user.nombre_usuario, user.correo_electronico, user.rol, 'Sí' if user.esta_activo else 'No'])
            
            writer.writerow([])
            writer.writerow(['=== PACIENTES ==='])
            writer.writerow(['ID', 'Nombre', 'Diagnóstico', 'Progreso', 'Sesiones'])
            for patient in Patient.query.all():
                writer.writerow([patient.id, patient.nombre_completo, patient.diagnostico or 'N/A', f'{patient.progreso}%', f'{patient.sesiones_completadas}/{patient.sesiones_totales}'])
            
            writer.writerow([])
            writer.writerow(['=== TERAPEUTAS ==='])
            writer.writerow(['ID', 'Nombre', 'Especialidad', 'Total Pacientes'])
            for therapist in Therapist.query.all():
                writer.writerow([therapist.id, therapist.nombre_completo, therapist.especialidad or 'N/A', therapist.total_pacientes])
            
            writer.writerow([])
            writer.writerow(['=== EJERCICIOS ==='])
            writer.writerow(['ID', 'Nombre', 'Categoría', 'Repeticiones'])
            for exercise in Exercise.query.all():
                writer.writerow([exercise.id, exercise.nombre, exercise.categoria or 'N/A', exercise.repeticiones or 'N/A'])
            
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
if current_user.rol == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.rol == 'therapist':
            return redirect(url_for('therapist_dashboard'))
        elif current_user.rol == 'patient':
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
    
    @app.route('/api/save-video-permanent', methods=['POST'])
    @login_required
    def save_video_permanent():
        """Guardar video permanente con audio de la sesión"""
        try:
            import os
            from app.models import SessionCapture
            
            if 'video' not in request.files:
                return jsonify({'success': False, 'message': 'No se recibió video'}), 400
            
            video_file = request.files['video']
            patient_id = request.form.get('patient_id')
            notes = request.form.get('notes', '')
            duration = request.form.get('duration', 0)
            is_permanent = request.form.get('permanent', 'false').lower() == 'true'
            
            if video_file.filename == '':
                return jsonify({'success': False, 'message': 'Archivo vacío'}), 400
            
            # Verificar permisos: solo terapeuta o paciente pueden guardar
            if current_user.rol not in ['therapist', 'patient']:
                return jsonify({'success': False, 'message': 'No tienes permisos para guardar videos'}), 403
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            role_prefix = 'terapeuta' if current_user.rol == 'therapist' else 'paciente'
            filename = f'video_permanente_{role_prefix}_{current_user.id}_{timestamp}.webm'
            
            # Crear ruta completa en carpeta permanente
            upload_folder = os.path.join('static', 'uploads', 'videos_permanentes')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            
            # Guardar archivo permanentemente
            video_file.save(file_path)
            
            # Obtener tamaño del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar en base de datos
            if current_user.rol == 'therapist':
                therapist = Therapist.query.filter_by(id_usuario=current_user.id).first()
                if not therapist:
                    return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
                
                capture = SessionCapture(
                    id_terapeuta=therapist.id,
                    id_paciente=patient_id if patient_id else None,
                    tipo_captura='video',
                    nombre_archivo=filename,
                    ruta_archivo=file_path,
                    tamano_archivo=file_size,
                    duracion=int(duration),
                    notas=notes,
                    es_permanente=is_permanent,
                    contiene_audio=True
                )
            else:  # patient
                patient = Patient.query.filter_by(id_usuario=current_user.id).first()
                if not patient:
                    return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
                
                capture = SessionCapture(
                    id_terapeuta=None,
                    id_paciente=patient.id,
                    tipo_captura='video',
                    nombre_archivo=filename,
                    ruta_archivo=file_path,
                    tamano_archivo=file_size,
                    duracion=int(duration),
                    notas=notes,
                    es_permanente=is_permanent,
                    contiene_audio=True
                )
            
            db.session.add(capture)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Video permanente guardado correctamente',
                'filename': filename,
                'file_path': file_path,
                'file_size': file_size,
                'duration': duration,
                'capture_id': capture.id,
                'created_at': capture.fecha_creacion.isoformat(),
                'is_permanent': is_permanent,
                'has_audio': True
            }), 200
                
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error al guardar video permanente: {str(e)}'}), 500

    @app.route('/api/save-video', methods=['POST'])
    @login_required
    @role_required('therapist')
    def save_video():
        """Guardar video grabado de la sesión (método antiguo para compatibilidad)"""
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
            therapist = Therapist.query.filter_by(id_usuario=current_user.id).first()
            if therapist:
                capture = SessionCapture(
                    id_terapeuta=therapist.id,
                    id_paciente=patient_id,
                    tipo_captura='video',
                    nombre_archivo=filename,
                    ruta_archivo=file_path,
                    tamano_archivo=file_size,
                    duracion=int(duration),
                    notas=notes
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
    def get_captures():
        """Obtener lista de capturas del terapeuta o paciente con control de acceso"""
        try:
            from app.models import SessionCapture
            
            if current_user.rol == 'therapist':
                therapist = Therapist.query.filter_by(id_usuario=current_user.id).first()
                if not therapist:
                    return jsonify({'success': False, 'message': 'Terapeuta no encontrado'}), 404
                
                # El terapeuta puede ver todas sus capturas y las de sus pacientes
                captures = SessionCapture.query.filter(
                    (SessionCapture.id_terapeuta == therapist.id) |
                    (SessionCapture.id_paciente.in_([p.id for p in therapist.pacientes_asignados]))
                ).order_by(SessionCapture.fecha_creacion.desc()).all()
                
            elif current_user.rol == 'patient':
                patient = Patient.query.filter_by(id_usuario=current_user.id).first()
                if not patient:
                    return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
                
                # El paciente solo puede ver sus propias capturas
                captures = SessionCapture.query.filter_by(id_paciente=patient.id).order_by(SessionCapture.fecha_creacion.desc()).all()
                
            else:
                return jsonify({'success': False, 'message': 'Rol no autorizado'}), 403
            
            captures_list = []
            for capture in captures:
                # Verificar permisos de acceso
                has_access = False
                if current_user.rol == 'therapist':
                    has_access = capture.id_terapeuta == therapist.id or capture.id_paciente in [p.id for p in therapist.pacientes_asignados]
                elif current_user.rol == 'patient':
                    has_access = capture.id_paciente == patient.id
                
                if has_access:
                    captures_list.append({
                        'id': capture.id,
                        'type': capture.tipo_captura,
                        'filename': capture.nombre_archivo,
                        'file_path': capture.ruta_archivo,
                        'file_size': capture.tamano_archivo,
                        'duration': capture.duracion,
                        'notes': capture.notas,
                        'patient_id': capture.id_paciente,
                        'therapist_id': capture.id_terapeuta,
                        'created_at': capture.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                        'is_permanent': capture.es_permanente,
                        'has_audio': capture.contiene_audio
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
                    'type': capture.tipo_captura,
                    'filename': capture.nombre_archivo,
                    'file_path': capture.ruta_archivo,
                    'file_size': capture.tamano_archivo,
                    'duration': capture.duracion,
                    'notes': capture.notas,
                    'created_at': capture.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                'success': True,
                'captures': captures_list,
                'total': len(captures_list)
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al obtener capturas: {str(e)}'}), 500

    # ============================================================
    # 📋 API PARA OBTENER DETALLES DE RUTINA (PACIENTE)
    # ============================================================
    @app.route('/api/get-routine-details/<int:routine_id>', methods=['GET'])
    @login_required
    @role_required('patient')
    def get_routine_details(routine_id):
        """Obtener detalles completos de una rutina"""
        try:
            from app.models import Routine, RoutineExercise
            
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if not patient:
                print(f"❌ Paciente no encontrado para user_id: {current_user.id}")
                return jsonify({'success': False, 'message': 'Paciente no encontrado'}), 404
            
            print(f"✓ Paciente encontrado: {patient.nombre_completo} (ID: {patient.id})")
            
            # Verificar que la rutina pertenece al paciente
            routine = Routine.query.filter_by(id=routine_id, patient_id=patient.id).first()
            if not routine:
                print(f"❌ Rutina {routine_id} no encontrada para paciente {patient.id}")
                return jsonify({'success': False, 'message': 'Rutina no encontrada'}), 404
            
print(f"✓ Rutina encontrada: {routine.nombre} (ID: {routine.id})")
            print(f"  Ejercicios en relación: {len(routine.ejercicios)}")
            
            # Obtener ejercicios de la rutina
            exercises_list = []
            for routine_ex in routine.exercises:
                exercise = routine_ex.ejercicio
                
                # Validar que el ejercicio existe
                if not exercise:
                    print(f"⚠️ Warning: Exercise ID {routine_ex.id_ejercicio} not found")
                    continue
                
print(f"  ✓ Agregando ejercicio: {exercise.nombre}")
                    exercises_list.append({
                        'id': exercise.id,
                        'name': exercise.nombre,
                        'description': exercise.descripcion or '',
                        'category': exercise.categoria or '',
'sets': routine_ex.series,
                    'repetitions': routine_ex.repeticiones,
                    'rest_seconds': routine_ex.segundos_descanso,
                    'notes': routine_ex.notas or '',
                    'order': routine_ex.orden
                })
            
            # Ordenar por orden
            exercises_list.sort(key=lambda x: x['order'])
            
            print(f"✓ Total ejercicios en respuesta: {len(exercises_list)}")
            
            response_data = {
                'success': True,
'routine': {
                    'id': routine.id,
                    'name': routine.nombre,
                    'description': routine.descripcion,
                    'duration_minutes': routine.duracion_minutos,
                    'difficulty': routine.dificultad,
                    'exercises': exercises_list
                }
            }
            
            print(f"✓ Enviando respuesta con {len(exercises_list)} ejercicios")
            return jsonify(response_data), 200
            
        except Exception as e:
            print(f"❌ Error en get_routine_details: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    # ============================================================
    # 📋 API PARA OBTENER PACIENTES (TERAPEUTA)
    # ============================================================
    @app.route('/api/get-patients', methods=['GET'])
    @login_required
    @role_required('therapist')
    def get_patients():
        """Obtener lista de pacientes activos"""
        try:
            patients = Patient.query.join(User).filter(User.is_active == True).all()
            
            patients_list = []
            for patient in patients:
                patients_list.append({
'id': patient.id,
                    'full_name': patient.nombre_completo,
                    'diagnosis': patient.diagnostico or 'Sin diagnóstico',
                    'progress': patient.progreso,
                    'completed_sessions': patient.sesiones_completadas,
                    'total_sessions': patient.sesiones_totales
                })
            
            return jsonify({
                'success': True,
                'patients': patients_list,
                'total': len(patients_list)
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    # ============================================================
    # LOGOUT
    # ============================================================
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sesión cerrada correctamente.', 'info')
        return redirect(url_for('login'))
