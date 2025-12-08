#!/usr/bin/env python3
"""
Script de verificación para la funcionalidad de compartir imágenes
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Therapist, Patient, SessionCapture, VideoShare

def verificar_compartir_imagenes():
    """Verificar que la funcionalidad de compartir imágenes está correctamente implementada"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("VERIFICACIÓN: Funcionalidad de Compartir Imágenes")
        print("=" * 70)
        print()
        
        # 1. Verificar que existen capturas de tipo 'photo'
        print("1️⃣ Verificando capturas de tipo 'photo'...")
        photos = SessionCapture.query.filter_by(tipo_captura='photo').all()
        print(f"   ✓ Encontradas {len(photos)} imágenes en el sistema")
        
        if photos:
            photo = photos[0]
            print(f"   📷 Ejemplo: {photo.nombre_archivo}")
            print(f"      - Terapeuta ID: {photo.id_terapeuta}")
            print(f"      - Paciente ID: {photo.id_paciente}")
            print(f"      - Fecha: {photo.fecha_creacion}")
        print()
        
        # 2. Verificar que existen videos compartidos
        print("2️⃣ Verificando videos/imágenes compartidos...")
        shares = VideoShare.query.all()
        print(f"   ✓ Encontrados {len(shares)} elementos compartidos")
        
        # Contar por tipo
        video_shares = 0
        photo_shares = 0
        for share in shares:
            if share.captura.tipo_captura == 'video':
                video_shares += 1
            elif share.captura.tipo_captura == 'photo':
                photo_shares += 1
        
        print(f"   🎥 Videos compartidos: {video_shares}")
        print(f"   📷 Imágenes compartidas: {photo_shares}")
        print()
        
        # 3. Verificar estructura de datos
        print("3️⃣ Verificando estructura de datos...")
        if shares:
            share = shares[0]
            print(f"   ✓ Campos en VideoShare:")
            print(f"      - id: {share.id}")
            print(f"      - id_captura: {share.id_captura}")
            print(f"      - id_terapeuta: {share.id_terapeuta}")
            print(f"      - id_paciente: {share.id_paciente}")
            print(f"      - mensaje: {share.mensaje[:50] if share.mensaje else 'N/A'}...")
            print(f"      - leido: {share.leido}")
            print(f"      - tipo_captura: {share.captura.tipo_captura}")
        print()
        
        # 4. Verificar relaciones
        print("4️⃣ Verificando relaciones...")
        therapists = Therapist.query.all()
        patients = Patient.query.all()
        
        print(f"   ✓ Terapeutas en el sistema: {len(therapists)}")
        print(f"   ✓ Pacientes en el sistema: {len(patients)}")
        
        if therapists and patients:
            therapist = therapists[0]
            patient = patients[0]
            
            # Capturas del terapeuta
            therapist_captures = SessionCapture.query.filter_by(id_terapeuta=therapist.id).all()
            therapist_photos = [c for c in therapist_captures if c.tipo_captura == 'photo']
            
            print(f"   📊 Terapeuta '{therapist.nombre_completo}':")
            print(f"      - Total capturas: {len(therapist_captures)}")
            print(f"      - Imágenes: {len(therapist_photos)}")
            
            # Capturas del paciente
            patient_captures = SessionCapture.query.filter_by(id_paciente=patient.id).all()
            patient_photos = [c for c in patient_captures if c.tipo_captura == 'photo']
            
            print(f"   📊 Paciente '{patient.nombre_completo}':")
            print(f"      - Total capturas: {len(patient_captures)}")
            print(f"      - Imágenes: {len(patient_photos)}")
        print()
        
        # 5. Resumen
        print("=" * 70)
        print("RESUMEN")
        print("=" * 70)
        print(f"✅ Total de imágenes en el sistema: {len(photos)}")
        print(f"✅ Total de elementos compartidos: {len(shares)}")
        print(f"   - Videos compartidos: {video_shares}")
        print(f"   - Imágenes compartidas: {photo_shares}")
        print()
        
        # 6. Recomendaciones
        print("📝 RECOMENDACIONES:")
        print()
        
        if len(photos) == 0:
            print("⚠️  No hay imágenes en el sistema")
            print("   → Captura algunas imágenes desde 'Iniciar Sesión' para probar")
            print()
        
        if photo_shares == 0:
            print("⚠️  No hay imágenes compartidas")
            print("   → Prueba compartir una imagen con un paciente")
            print()
        else:
            print("✅ La funcionalidad de compartir imágenes está funcionando")
            print()
        
        # 7. Instrucciones de prueba
        print("=" * 70)
        print("CÓMO PROBAR")
        print("=" * 70)
        print()
        print("1. Como Terapeuta:")
        print("   a) Ir a 'Galería de Videos'")
        print("   b) Buscar una imagen (ícono 📷)")
        print("   c) Hacer clic en 'Compartir con Paciente'")
        print("   d) Seleccionar un paciente")
        print("   e) Agregar un mensaje opcional")
        print("   f) Hacer clic en 'Compartir Imagen'")
        print()
        print("2. Como Paciente:")
        print("   a) Ir a 'Galería de Videos'")
        print("   b) Hacer clic en 'Contenido Compartido'")
        print("   c) Ver las imágenes compartidas")
        print("   d) Hacer clic en 'Ver' para visualizar")
        print()
        print("=" * 70)

if __name__ == '__main__':
    try:
        verificar_compartir_imagenes()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
