#!/bin/bash

# Script de despliegue mejorado para AWS EC2
# Autor: Sistema Dulcería Lilis
# Fecha: 2025-11-22

set -e  # Detener si hay errores

echo "🚀 Iniciando despliegue..."

# Guardar el directorio actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📥 Descargando cambios desde GitHub..."
# Descartar cambios locales y actualizar desde main
git fetch origin
git reset --hard origin/main
git pull origin main

echo "📦 Instalando dependencias..."
source venv/bin/activate
pip install -r requirements.txt --quiet

echo "🗄️  Aplicando migraciones..."
python manage.py migrate --noinput

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🔄 Reiniciando servidor..."
sudo systemctl daemon-reload
sudo systemctl restart dulceria

echo "✅ ¡Despliegue completado exitosamente!"
echo ""
echo "📊 Estado del servicio:"
sudo systemctl status dulceria --no-pager -l
