"""
Script para verificar que los videos compartidos se pueden reproducir
"""
from app import create_app, db
from app.models import User, Patient, Therapist, SessionCapture, VideoShare
import os

app = create_app()

with app.app_context():
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DE VIDEOS COMPARTIDOS")
    print("=" * 70)
    
    # Verificar paciente
    print("\n1️⃣ Verificando paciente...")
    paciente_user = User.query.filter_by(nombre_usuario='paciente').first()
    
    if not paciente_user:
        print("❌ Usuario paciente no existe")
        exit(1)
    
    paciente = Patient.query.filter_by(id_usuario=paciente_user.id).first()
    if not paciente:
        print("❌ Perfil de paciente no existe")
        exit(1)
    
    print(f"✅ Paciente: {paciente.nombre_completo}")
    
    # Verificar videos compartidos
    print("\n2️⃣ Verificando videos compartidos con el paciente...")
    videos_compartidos = VideoShare.query.filter_by(id_paciente=paciente.id).all()
    
    print(f"   Total de videos compartidos: {len(videos_compartidos)}")
    
    if len(videos_compartidos) == 0:
        print("\n⚠️ No hay videos compartidos con este paciente")
        print("\n🔧 SOLUCIÓN:")
        print("   1. Login como terapeuta")
        print("   2. Ve a Galería de Videos")
        print("   3. Click en 'Compartir con Paciente' en un video")
        print("   4. Selecciona al paciente")
        print("   5. Comparte el video")
        exit(0)
    
    print("\n📹 VIDEOS COMPARTIDOS:")
    print("-" * 70)
    
    for idx, share in enumerate(videos_compartidos, 1):
        captura = share.captura
        terapeuta = share.terapeuta
        
        print(f"\n{idx}. Video compartido:")
        print(f"   ID: {share.id}")
        print(f"   Terapeuta: {terapeuta.nombre_completo}")
        print(f"   Fecha: {share.fecha_compartido}")
        print(f"   Leído: {'Sí' if share.leido else 'No'}")
        print(f"   Mensaje: {share.mensaje or '(sin mensaje)'}")
        
        print(f"\n   Información del video:")
        print(f"   - Nombre: {captura.nombre_archivo}")
        print(f"   - Ruta: {captura.ruta_archivo}")
        print(f"   - Duración: {captura.duracion}s")
        print(f"   - Tamaño: {captura.tamano_archivo} bytes")
        print(f"   - Audio: {'Sí' if captura.contiene_audio else 'No'}")
        
        # Verificar que el archivo existe
        if captura.ruta_archivo.startswith('/static/'):
            # Convertir ruta web a ruta del sistema
            ruta_relativa = captura.ruta_archivo.replace('/static/', 'static/')
            ruta_completa = os.path.join(os.getcwd(), ruta_relativa)
            
            if os.path.exists(ruta_completa):
                print(f"   ✅ Archivo existe en: {ruta_completa}")
            else:
                print(f"   ❌ Archivo NO existe en: {ruta_completa}")
                print(f"      El video no se podrá reproducir")
        else:
            print(f"   ⚠️ Ruta no estándar: {captura.ruta_archivo}")
    
    # Simular respuesta de la API
    print("\n" + "=" * 70)
    print("3️⃣ Simulando respuesta de la API /api/get-shared-videos")
    print("=" * 70)
    
    videos_list = []
    for share in videos_compartidos:
        videos_list.append({
            'id': share.id,
            'capture_id': share.id_captura,
            'filename': share.captura.nombre_archivo,
            'file_path': share.captura.ruta_archivo,
            'file_size': share.captura.tamano_archivo,
            'duration': share.captura.duracion,
            'therapist_name': share.terapeuta.nombre_completo,
            'message': share.mensaje,
            'fecha_compartido': share.fecha_compartido.strftime('%Y-%m-%d %H:%M:%S'),
            'leido': share.leido,
            'has_audio': share.captura.contiene_audio
        })
    
    import json
    print(json.dumps({
        'success': True,
        'videos': videos_list,
        'total': len(videos_list)
    }, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("   1. Asegúrate de que el servidor Flask esté corriendo")
    print("   2. Login como paciente (paciente / paci123)")
    print("   3. Ve a Galería de Videos → Videos Compartidos")
    print("   4. Abre DevTools (F12) → Console")
    print("   5. Intenta reproducir un video")
    print("   6. Observa los mensajes en la consola")
    
    print("\n💡 QUÉ BUSCAR EN LA CONSOLA:")
    print("   - Errores de 'file not found' (404)")
    print("   - Errores de 'playSharedVideoFromData is not defined'")
    print("   - Errores de 'Cannot read property'")
    
    print("\n📋 SI EL VIDEO NO SE REPRODUCE:")
    print("   1. Verifica que el archivo existe (arriba)")
    print("   2. Verifica que la ruta sea correcta")
    print("   3. Verifica que el navegador soporte WebM")
    print("   4. Intenta descargar el video primero")
    
    print("\n" + "=" * 70)
