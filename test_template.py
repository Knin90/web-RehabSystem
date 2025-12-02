"""Test del template export_data"""
from app import create_app
from app.models import User, Patient, Therapist, Exercise

app = create_app()

with app.app_context():
    try:
        # Simular la ruta
        stats = {
            'total_users': User.query.count(),
            'total_patients': Patient.query.count(),
            'total_therapists': Therapist.query.count(),
            'total_exercises': Exercise.query.count()
        }
        
        print("=== ESTADÍSTICAS ===")
        print(f"Usuarios: {stats['total_users']}")
        print(f"Pacientes: {stats['total_patients']}")
        print(f"Terapeutas: {stats['total_therapists']}")
        print(f"Ejercicios: {stats['total_exercises']}")
        
        # Intentar renderizar el template
        from flask import render_template
        from app.models import SystemSettings
        
        html = render_template('admin/export_data.html', 
                             active_page='export',
                             total_users=stats['total_users'],
                             total_patients=stats['total_patients'],
                             total_therapists=stats['total_therapists'],
                             total_exercises=stats['total_exercises'],
                             system_theme=SystemSettings.get_setting('theme', 'light'),
                             system_language=SystemSettings.get_setting('language', 'es'),
                             system_compact=SystemSettings.get_setting('compact_mode', 'off'))
        
        print("\n✅ Template renderizado correctamente")
        print(f"Tamaño del HTML: {len(html)} bytes")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
