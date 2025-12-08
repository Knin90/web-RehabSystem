"""
Script para verificar la ruta exacta del video compartido
"""
from app import create_app, db
from app.models import VideoShare, Patient, User
import os

app = create_app()

with app.app_context():
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DE RUTA DE VIDEO")
    print("=" * 70)
    
    # Obtener paciente
    paciente_user = User.query.filter_by(nombre_usuario='paciente').first()
    if not paciente_user:
        print("❌ Usuario paciente no existe")
        exit(1)
    
    paciente = Patient.query.filter_by(id_usuario=paciente_user.id).first()
    if not paciente:
        print("❌ Perfil de paciente no existe")
        exit(1)
    
    # Obtener videos compartidos
    videos = VideoShare.query.filter_by(id_paciente=paciente.id).all()
    
    if len(videos) == 0:
        print("❌ No hay videos compartidos")
        exit(1)
    
    print(f"\n✅ Encontrados {len(videos)} video(s) compartido(s)\n")
    
    for idx, share in enumerate(videos, 1):
        captura = share.captura
        
        print(f"{'=' * 70}")
        print(f"VIDEO {idx}: {captura.nombre_archivo}")
        print(f"{'=' * 70}")
        
        print(f"\n📋 Información de la base de datos:")
        print(f"   - ID Captura: {captura.id}")
        print(f"   - Nombre archivo: {captura.nombre_archivo}")
        print(f"   - Ruta en BD: {captura.ruta_archivo}")
        print(f"   - Duración: {captura.duracion}s")
        print(f"   - Tamaño: {captura.tamano_archivo} bytes")
        
        # Verificar diferentes rutas posibles
        print(f"\n🔍 Verificando existencia del archivo:")
        
        # Ruta 1: Como está en la BD
        ruta_bd = captura.ruta_archivo
        print(f"\n   1. Ruta en BD: {ruta_bd}")
        
        # Ruta 2: Convertir /static/ a static/
        if ruta_bd.startswith('/static/'):
            ruta_relativa = ruta_bd.replace('/static/', 'static/')
            ruta_completa = os.path.join(os.getcwd(), ruta_relativa)
            
            print(f"   2. Ruta relativa: {ruta_relativa}")
            print(f"   3. Ruta completa: {ruta_completa}")
            
            if os.path.exists(ruta_completa):
                print(f"   ✅ ARCHIVO EXISTE")
                print(f"   📁 Tamaño real: {os.path.getsize(ruta_completa)} bytes")
            else:
                print(f"   ❌ ARCHIVO NO EXISTE")
                
                # Buscar el archivo en otras ubicaciones
                print(f"\n   🔍 Buscando archivo en otras ubicaciones...")
                
                # Buscar en static/captures/
                captures_dir = os.path.join(os.getcwd(), 'static', 'captures')
                if os.path.exists(captures_dir):
                    archivos = os.listdir(captures_dir)
                    print(f"   📁 Archivos en static/captures/:")
                    for archivo in archivos:
                        if archivo.endswith('.webm'):
                            print(f"      - {archivo}")
                else:
                    print(f"   ❌ Directorio static/captures/ no existe")
        
        # Verificar URL accesible
        print(f"\n🌐 URL para el navegador:")
        print(f"   {ruta_bd}")
        print(f"\n   Para verificar en el navegador:")
        print(f"   http://localhost:5000{ruta_bd}")
        
        print(f"\n💡 SOLUCIÓN:")
        if not os.path.exists(ruta_completa):
            print(f"   El archivo no existe. Opciones:")
            print(f"   1. El terapeuta debe grabar un nuevo video")
            print(f"   2. O actualizar la ruta en la base de datos")
        else:
            print(f"   El archivo existe. El problema puede ser:")
            print(f"   1. Permisos del archivo")
            print(f"   2. El navegador no soporta WebM")
            print(f"   3. Error en el JavaScript")
    
    print(f"\n{'=' * 70}")
    print("✅ VERIFICACIÓN COMPLETADA")
    print(f"{'=' * 70}")
