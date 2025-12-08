#!/bin/bash
# Script de inicio para Render
# Inicializa la base de datos y luego inicia gunicorn

echo "Inicializando base de datos..."
python init_db_auto.py

echo "Iniciando gunicorn..."
gunicorn run:app --bind 0.0.0.0:$PORT
