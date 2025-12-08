"""
Script para verificar que el sistema esté correctamente configurado
"""
import sys
import os

def verificar_importaciones():
    """Verificar que todos los módulos se importen correctamente"""
    print("=" * 60)
    print("1. VERIFICANDO IMPORTACIONES")
    print("=" * 60)
    
    try:
        from app import create_app, db
        print("✓ app importado correctamente")
        
        from app.models import User, Patient, Therapist, Exercise, Routine, RoutineExercise, SessionCapture
        print("✓ Todos los modelos importados correctamente")
        
        from app.routes import register_routes
        print("✓ Rutas importadas correctamente")
        
        from app.forms import LoginForm
        print("✓ Formularios importados correctamente")
        
        return True
    except Exception as e:
        print(f"✗ Error en importaciones: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_app():
    """Verificar que la aplicación se cree correctamente"""
    print("\n" + "=" * 60)
    print("2. VERIFICANDO CREACIÓN DE APLICACIÓN")
    print("=" * 60)
    
    try:
        from app import create_app
        app = create_app()
        print("✓ Aplicación creada correctamente")
        print(f"  - Nombre: {app.name}")
        print(f"  - Debug: {app.debug}")
        print(f"  - Secret Key configurado: {'Sí' if app.config.get('SECRET_KEY') else 'No'}")
        return True
    except Exception as e:
        print(f"✗ Error al crear aplicación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_modelos():
    """Verificar que los modelos tengan los atributos correctos"""
    print("\n" + "=" * 60)
    print("3. VERIFICANDO MODELOS")
    print("=" * 60)
    
    try:
        from app.models import User, Patient, Therapist, Exercise, Routine, SessionCapture
        
        # Verificar User
        user_attrs = ['nombre_usuario', 'correo_electronico', 'contrasena_encriptada', 'rol', 'esta_activo']
        for attr in user_attrs:
            if hasattr(User, attr):
                print(f"✓ User.{attr}")
            else:
                print(f"✗ User.{attr} NO ENCONTRADO")
                return False
        
        # Verificar Patient
        patient_attrs = ['id_usuario', 'nombre_completo', 'diagnostico', 'progreso', 'sesiones_totales', 'sesiones_completadas']
        for attr in patient_attrs:
            if hasattr(Patient, attr):
                print(f"✓ Patient.{attr}")
            else:
                print(f"✗ Patient.{attr} NO ENCONTRADO")
                return False
        
        # Verificar Therapist
        therapist_attrs = ['id_usuario', 'nombre_completo', 'especialidad', 'total_pacientes']
        for attr in therapist_attrs:
            if hasattr(Therapist, attr):
                print(f"✓ Therapist.{attr}")
            else:
                print(f"✗ Therapist.{attr} NO ENCONTRADO")
                return False
        
        # Verificar Exercise
        exercise_attrs = ['nombre', 'descripcion', 'categoria', 'repeticiones']
        for attr in exercise_attrs:
            if hasattr(Exercise, attr):
                print(f"✓ Exercise.{attr}")
            else:
                print(f"✗ Exercise.{attr} NO ENCONTRADO")
                return False
        
        # Verificar SessionCapture
        capture_attrs = ['id_terapeuta', 'id_paciente', 'tipo_captura', 'nombre_archivo', 'ruta_archivo', 'notas']
        for attr in capture_attrs:
            if hasattr(SessionCapture, attr):
                print(f"✓ SessionCapture.{attr}")
            else:
                print(f"✗ SessionCapture.{attr} NO ENCONTRADO")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error al verificar modelos: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    print("\n" + "=" * 60)
    print("4. VERIFICANDO DEPENDENCIAS")
    print("=" * 60)
    
    dependencias = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_bcrypt',
        'flask_migrate',
        'dotenv'
    ]
    
    todas_ok = True
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} NO INSTALADO")
            todas_ok = False
    
    return todas_ok

def verificar_archivos():
    """Verificar que existan los archivos necesarios"""
    print("\n" + "=" * 60)
    print("5. VERIFICANDO ARCHIVOS")
    print("=" * 60)
    
    archivos_necesarios = [
        'app/__init__.py',
        'app/models.py',
        'app/routes.py',
        'app/forms.py',
        'app/config.py',
        'run.py',
        'requirements.txt',
        '.env'
    ]
    
    todos_ok = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✓ {archivo}")
        else:
            print(f"✗ {archivo} NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "VERIFICACIÓN DEL SISTEMA REHAB" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    resultados = []
    
    # Ejecutar verificaciones
    resultados.append(("Importaciones", verificar_importaciones()))
    resultados.append(("Aplicación", verificar_app()))
    resultados.append(("Modelos", verificar_modelos()))
    resultados.append(("Dependencias", verificar_dependencias()))
    resultados.append(("Archivos", verificar_archivos()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    total = len(resultados)
    exitosos = sum(1 for _, ok in resultados if ok)
    
    for nombre, ok in resultados:
        estado = "✓ PASS" if ok else "✗ FAIL"
        print(f"{nombre:20} {estado}")
    
    print("\n" + "-" * 60)
    print(f"Total: {exitosos}/{total} verificaciones exitosas")
    print("-" * 60)
    
    if exitosos == total:
        print("\n✅ SISTEMA VERIFICADO CORRECTAMENTE")
        print("El sistema está listo para ejecutarse.")
        return 0
    else:
        print("\n❌ SISTEMA CON ERRORES")
        print("Por favor, revisa los errores anteriores.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
