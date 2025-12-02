"""Script para probar las configuraciones del sistema"""
from app import create_app, db
from app.models import SystemSettings

app = create_app()

with app.app_context():
    print("=== CONFIGURACIONES ACTUALES ===\n")
    
    settings_to_check = [
        ('theme', 'Tema'),
        ('language', 'Idioma'),
        ('session_duration', 'Duración de sesión'),
        ('sessions_per_week', 'Sesiones por semana'),
        ('email_notifications', 'Notificaciones email'),
        ('detection_accuracy', 'Precisión detección'),
    ]
    
    for key, label in settings_to_check:
        value = SystemSettings.get_setting(key, 'No configurado')
        print(f"{label:25} : {value}")
    
    print("\n=== PRUEBA DE GUARDADO ===\n")
    
    # Cambiar tema a oscuro
    SystemSettings.set_setting('theme', 'dark')
    print(f"✅ Tema cambiado a: {SystemSettings.get_setting('theme')}")
    
    # Cambiar idioma a inglés
    SystemSettings.set_setting('language', 'en')
    print(f"✅ Idioma cambiado a: {SystemSettings.get_setting('language')}")
    
    # Restaurar valores
    SystemSettings.set_setting('theme', 'light')
    SystemSettings.set_setting('language', 'es')
    print(f"\n✅ Valores restaurados")
    print(f"   Tema: {SystemSettings.get_setting('theme')}")
    print(f"   Idioma: {SystemSettings.get_setting('language')}")
