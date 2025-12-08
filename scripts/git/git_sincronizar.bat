@echo off
echo ========================================
echo SINCRONIZAR CON GITHUB
echo ========================================
echo.
echo Este script va a:
echo 1. Descargar cambios de GitHub
echo 2. Fusionarlos con tus cambios locales
echo 3. Subir todo a GitHub
echo.
pause
echo.

echo Paso 1: Descargar cambios de GitHub...
git pull origin main --no-rebase

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo HAY CONFLICTOS
    echo ========================================
    echo.
    echo Git encontró conflictos al fusionar.
    echo Necesitas resolverlos manualmente.
    echo.
    echo Archivos con conflicto:
    git status --short
    echo.
    echo Para resolver:
    echo 1. Abre cada archivo con conflicto
    echo 2. Busca las lineas con ^<^<^<^<^<^<^< HEAD
    echo 3. Decide que codigo mantener
    echo 4. Elimina las marcas de conflicto
    echo 5. Guarda el archivo
    echo 6. Ejecuta:
    echo    git add .
    echo    git commit -m "Resolver conflictos"
    echo    git push origin main
    echo.
    pause
    exit /b 1
)

echo.
echo Paso 2: Verificar estado...
git status

echo.
echo Paso 3: Subir cambios a GitHub...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo EXITO!
    echo ========================================
    echo.
    echo Tus cambios se han subido correctamente a GitHub.
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR AL SUBIR
    echo ========================================
    echo.
    echo Hubo un error al subir los cambios.
    echo Revisa los mensajes de error arriba.
    echo.
)

pause
