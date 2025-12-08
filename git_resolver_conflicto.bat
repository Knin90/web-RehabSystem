@echo off
echo ========================================
echo RESOLVER CONFLICTO DE GIT
echo ========================================
echo.
echo El error dice que hay cambios en GitHub que no tienes localmente.
echo.
echo Este script va a:
echo 1. Descargar los cambios de GitHub
echo 2. Intentar fusionarlos automáticamente
echo 3. Subir tus cambios
echo.
pause
echo.

echo Paso 1: Descargar cambios de GitHub...
git pull origin main --no-rebase

echo.
echo Verificando estado...
git status

echo.
echo ========================================
echo.
echo Si hay conflictos, Git te lo dirá arriba.
echo.
echo Si NO hay conflictos:
echo   - Ejecuta: git_push_corregido.bat
echo.
echo Si HAY conflictos:
echo   - Abre los archivos marcados con conflicto
echo   - Resuelve los conflictos manualmente
echo   - Luego ejecuta:
echo     git add .
echo     git commit -m "Resolver conflictos"
echo     git push origin main
echo.
pause
