#!/bin/bash
# Script de inicio para Render
# Inicializa la base de datos y luego inicia gunicorn

echo "=========================================="
echo "INICIANDO REHABSYSTEM"
echo "=========================================="

echo ""
echo "Paso 1: Verificando variables de entorno..."
echo "FLASK_ENV: $FLASK_ENV"
echo "DATABASE_URL: ${DATABASE_URL:0:30}..." # Solo mostrar inicio

echo ""
echo "Paso 2: Inicializando base de datos..."
python init_db_auto.py
INIT_EXIT_CODE=$?

if [ $INIT_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Advertencia: Inicialización retornó código $INIT_EXIT_CODE"
    echo "Continuando de todas formas..."
fi

echo ""
echo "Paso 3: Iniciando gunicorn..."
echo "=========================================="
gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
