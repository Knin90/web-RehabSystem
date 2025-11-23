from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta_rehab_sistema_2024'

# Usuarios demo del sistema
USUARIOS_DEMO = {
    'admin': {'password': 'admin123', 'rol': 'admin', 'nombre': 'Administrador Principal'},
    'terapeuta': {'password': 'tera123', 'rol': 'terapeuta', 'nombre': 'Rafael Lu'}, 
    'paciente': {'password': 'paci123', 'rol': 'paciente', 'nombre': 'Andrea Luna'}
}

# Datos demo específicos para paciente
DATOS_PACIENTE = {
    'paciente': {
        'nombre_completo': 'Andrea Luna',
        'edad': 28,
        'diagnostico': 'Rehabilitación post-quirúrgica rodilla derecha',
        'fecha_ingreso': '2024-08-15',
        'terapeutas': [
            {'nombre': 'Dra. Yolenis Guarnán', 'especialidad': 'Fisioterapeuta', 'telefono': '+507 6123-4567'},
            {'nombre': 'Dr. Carlos Rodríguez', 'especialidad': 'Traumatólogo', 'telefono': '+507 6987-6543'}
        ],
        'progreso': 75,
        'sesiones_completadas': 12,
        'sesiones_totales': 16,
        'citas_proximas': [
            {'fecha': '2024-11-22', 'dia': 'Viernes', 'terapeuta': 'Dra. Yolenis Guarnán', 'hora': '10:00 AM', 'tipo': 'Terapia física'},
            {'fecha': '2024-11-29', 'dia': 'Viernes', 'terapeuta': 'Dra. Yolenis Guarnán', 'hora': '10:00 AM', 'tipo': 'Evaluación de progreso'}
        ],
        'recordatorios': [
            {'mensaje': 'Recordar próxima cita 22 de noviembre', 'terapeuta': 'Dra. Yolenis Guarnán', 'tiempo': 'Hace 1 minuto'}
        ],
        'ejercicios_asignados': [
            {'nombre': 'Flexiones de rodilla', 'repeticiones': '3 series de 15', 'estado': 'Completado'},
            {'nombre': 'Elevaciones de pierna', 'repeticiones': '3 series de 12', 'estado': 'Pendiente'},
            {'nombre': 'Estiramiento cuádriceps', 'repeticiones': '4 series de 30 seg', 'estado': 'Completado'},
            {'nombre': 'Sentadillas asistidas', 'repeticiones': '3 series de 10', 'estado': 'En progreso'}
        ]
    }
}

# Datos demo específicos para terapeuta
DATOS_TERAPEUTA = {
    'terapeuta': {
        'nombre_completo': 'Rafael Lu',
        'especialidad': 'Fisioterapeuta Especialista',
        'email': 'lu_raf@rehabsystem.com',
        'telefono': '+507 6123-4567',
        'pacientes_total': 24,
        'pacientes_activos': 12,
        'citas_hoy': 8,
        'evaluaciones_pendientes': 3,
        'estadisticas': {
            'progreso_promedio': 68,
            'sesiones_mes': 45,
            'pacientes_nuevos': 5
        },
        'citas_proximas': [
            {'fecha': '2024-11-22', 'dia': 'Viernes', 'paciente': 'Carlos Rodríguez', 'hora': '9:00 AM', 'sala': 'Sala 2'},
            {'fecha': '2024-11-22', 'dia': 'Viernes', 'paciente': 'María González', 'hora': '11:00 AM', 'sala': 'Sala 1'},
            {'fecha': '2024-11-23', 'dia': 'Sábado', 'paciente': 'Ana Martínez', 'hora': '10:00 AM', 'sala': 'Sala 3'}
        ],
        'mensajes': [
            {'remitente': 'Dr. Ansel Sanjar', 'mensaje': 'Paciente con rotura de ligamento sala 3', 'tiempo': 'Hace 1 minuto', 'urgente': True},
            {'remitente': 'Dra. Laura Méndez', 'mensaje': 'Reunión de equipo a las 3 PM', 'tiempo': 'Hace 15 minutos', 'urgente': False},
            {'remitente': 'Sistema', 'mensaje': 'Evaluaciones pendientes: 3 pacientes', 'tiempo': 'Hace 2 horas', 'urgente': False}
        ],
        'pacientes_recientes': [
            {'nombre': 'Andrea Luna', 'progreso': 75, 'ultima_sesion': '2024-11-20', 'proxima_cita': '2024-11-25'},
            {'nombre': 'Juan Pérez', 'progreso': 45, 'ultima_sesion': '2024-11-19', 'proxima_cita': '2024-11-26'},
            {'nombre': 'María García', 'progreso': 90, 'ultima_sesion': '2024-11-18', 'proxima_cita': '2024-11-24'}
        ]
    }
}

# Datos demo específicos para admin
DATOS_ADMIN = {
    'admin': {
        'nombre_completo': 'Administrador Principal',
        'email': 'admin@rehabsystem.com',
        'estadisticas': {
            'usuarios_totales': 156,
            'terapeutas_activos': 24,
            'pacientes_activos': 132,
            'citas_hoy': 45
        }
    }
}

@app.route('/')
def index():
    # Limpiar sesión si vienen del logout
    if 'from_logout' in request.args:
        session.clear()
    return render_template('index.html')

@app.route('/seleccionar-modulo')
def seleccionar_modulo():
    # Si ya está logueado, ir al dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('seleccionar_modulo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    modulo_seleccionado = request.args.get('modulo', '')
    
    # Si no hay módulo seleccionado, redirigir a selección
    if not modulo_seleccionado and request.method == 'GET':
        return redirect(url_for('seleccionar_modulo'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        modulo = request.form.get('modulo', '')
        
        # Validar credenciales
        if username in USUARIOS_DEMO and USUARIOS_DEMO[username]['password'] == password:
            rol_usuario = USUARIOS_DEMO[username]['rol']
            
            # Verificar que el rol coincida con el módulo seleccionado
            if modulo and rol_usuario != modulo:
                flash('No tiene permisos para acceder a este módulo.', 'error')
                return render_template('login.html', modulo_seleccionado=modulo)
            
            # Iniciar sesión
            session['user'] = username
            session['rol'] = USUARIOS_DEMO[username]['rol']
            session['nombre'] = USUARIOS_DEMO[username]['nombre']
            
            flash(f'¡Bienvenido/a {session["nombre"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas. Por favor, intente nuevamente.', 'error')
    
    return render_template('login.html', modulo_seleccionado=modulo_seleccionado)

@app.route('/dashboard')
def dashboard():
    # Si no está logueado, redirigir a selección de módulo
    if 'user' not in session:
        flash('Por favor, inicie sesión para acceder al dashboard.', 'warning')
        return redirect(url_for('seleccionar_modulo'))
    
    # Cargar datos específicos según el rol
    usuario_actual = {
        'username': session['user'],
        'rol': session['rol'],
        'nombre': session['nombre']
    }
    
    # Cargar datos específicos según el rol
    datos_extra = {}
    template_name = 'dashboard_base.html'
    
    if session['rol'] == 'paciente' and session['user'] in DATOS_PACIENTE:
        datos_extra = DATOS_PACIENTE[session['user']]
        template_name = 'dashboard_paciente.html'
    elif session['rol'] == 'terapeuta' and session['user'] in DATOS_TERAPEUTA:
        datos_extra = DATOS_TERAPEUTA[session['user']]
        template_name = 'dashboard_terapeuta.html'
    elif session['rol'] == 'admin' and session['user'] in DATOS_ADMIN:
        datos_extra = DATOS_ADMIN[session['user']]
        template_name = 'dashboard_admin.html'
    
    return render_template(template_name, usuario=usuario_actual, datos=datos_extra)

@app.route('/logout')
def logout():
    nombre_usuario = session.get('nombre', 'Usuario')
    session.clear()
    flash(f'Sesión cerrada correctamente. ¡Hasta pronto, {nombre_usuario}!', 'info')
    # Redirigir al inicio con parámetro para limpiar sesión
    return redirect(url_for('index', from_logout='true'))

# Ruta para limpiar sesión manualmente
@app.route('/clear-session')
def clear_session():
    session.clear()
    flash('Sesión limpiada correctamente.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)