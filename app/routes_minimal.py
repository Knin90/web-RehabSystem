from flask import render_template, redirect, url_for, flash, request
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

    @app.route('/therapist/video-gallery')
    @login_required
    @role_required('therapist')
    def therapist_video_gallery():
        return render_template('therapist/video_gallery.html', active_page='video_gallery')

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
            flash(f"Error al cargar rutinas: {str(e)}", 'danger')
            return redirect(url_for('therapist_dashboard'))

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
        active_therapists = sum(1 for t in therapists if t.usuario.esta_activo)
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
        active_patients = sum(1 for p in patients if p.usuario.esta_activo)
        in_therapy = sum(1 for p in patients if p.sesiones_completadas < p.sesiones_totales and p.usuario.esta_activo)
        return render_template('admin/patients.html', 
                             active_page='patients',
                             patients=patients,
                             active_patients=active_patients,
                             in_therapy=in_therapy,
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))

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
    # LOGOUT
    # ============================================================
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sesión cerrada correctamente.', 'info')
        return redirect(url_for('login'))