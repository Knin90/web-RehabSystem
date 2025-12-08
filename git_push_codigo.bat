@echo off
echo ========================================
echo SUBIR CAMBIOS DE CODIGO A GITHUB
echo ========================================
echo.
echo Este script subirá solo los archivos de código
echo (sin archivos .md de documentación)
echo.
pause
echo.

cd web-RehabSystem

echo Agregando archivos de código...
git add app/routes.py
git add app/models.py
git add app/__init__.py
git add templates/patient/video_gallery.html
git add templates/therapist/video_gallery.html
git add requirements.txt

echo.
echo Agregando scripts de Python...
git add setup_complete.py
git add verificar_pacientes.py
git add test_api_simple.py
git add test_shared_video_playback.py
git add verificar_ruta_video.py

echo.
echo Agregando archivos HTML de test...
git add test_botones_simple.html
git add test_video_buttons.html

echo.
echo Archivos agregados. Creando commit...
git commit -m "feat: Agregar funcionalidad completa de videos compartidos

- Implementar reproducción y descarga de videos
- Agregar pestañas para videos compartidos (paciente y terapeuta)
- Implementar control de velocidad de reproducción (0.5x, 1x, 1.5x, 2x)
- Agregar modo pantalla completa
- Implementar sistema de compartir videos bidireccional
- Agregar notificaciones de videos no leídos
- Usar atributos data-* para evitar problemas de escape
- Agregar logs de debug extensivos
- Corregir errores de sintaxis en JavaScript"

echo.
echo Subiendo a GitHub...
git push origin main

echo.
echo ========================================
echo LISTO!
echo ========================================
echo.
echo Los cambios de código han sido subidos a GitHub
echo (sin archivos .md de documentación)
echo.
pause
