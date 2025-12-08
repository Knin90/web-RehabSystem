@echo off
echo ========================================
echo VER CAMBIOS EN ARCHIVOS DE CODIGO
echo ========================================
echo.

cd web-RehabSystem

echo Archivos modificados:
echo.
git status --short

echo.
echo ========================================
echo Archivos de código que se subirán:
echo ========================================
echo.
echo BACKEND:
echo   - app/routes.py
echo   - app/models.py
echo   - app/__init__.py
echo.
echo FRONTEND:
echo   - templates/patient/video_gallery.html
echo   - templates/therapist/video_gallery.html
echo.
echo SCRIPTS:
echo   - setup_complete.py
echo   - verificar_pacientes.py
echo   - test_api_simple.py
echo   - test_shared_video_playback.py
echo   - verificar_ruta_video.py
echo.
echo TESTS:
echo   - test_botones_simple.html
echo   - test_video_buttons.html
echo.
echo OTROS:
echo   - requirements.txt
echo.
echo ========================================
echo.
pause
