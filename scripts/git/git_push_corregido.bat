@echo off
echo ========================================
echo SUBIR CAMBIOS DE CODIGO A GITHUB
echo ========================================
echo.
echo Este script:
echo 1. Descargará cambios de GitHub
echo 2. Subirá tus cambios de código
echo.
pause
echo.

echo Paso 1: Descargar cambios de GitHub...
git pull origin main

echo.
echo Paso 2: Agregar archivos de código...
git add app/routes.py
git add app/models.py
git add app/__init__.py
git add ../templates/patient/video_gallery.html
git add ../templates/therapist/video_gallery.html
git add setup_complete.py
git add verificar_pacientes.py
git add test_api_simple.py
git add test_shared_video_playback.py
git add verificar_ruta_video.py
git add test_botones_simple.html
git add test_video_buttons.html
git add requirements.txt

echo.
echo Paso 3: Crear commit...
git commit -m "feat: Agregar funcionalidad completa de videos compartidos - Implementar reproduccion y descarga de videos - Agregar pestanas para videos compartidos - Implementar control de velocidad - Agregar modo pantalla completa - Sistema bidireccional de compartir videos - Notificaciones de videos no leidos - Usar atributos data para evitar errores - Agregar logs de debug - Corregir errores de sintaxis JavaScript"

echo.
echo Paso 4: Subir a GitHub...
git push origin main

echo.
echo ========================================
echo LISTO!
echo ========================================
echo.
pause
