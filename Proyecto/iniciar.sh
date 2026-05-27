#!/bin/bash
# PrivaScanner - Script de inicio para macOS / Linux
# Uso: bash iniciar.sh  (o: chmod +x iniciar.sh && ./iniciar.sh)

set -e

echo "=================================================="
echo " PrivaScanner v1.0 - Script de inicio"
echo " Sistema: $(uname -s)"
echo "=================================================="
echo ""

# Ir al directorio del script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"

cd "$BACKEND_DIR" || { echo "[ERROR] No se encontró el directorio backend"; exit 1; }

# Verificar que Python 3 esté instalado
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 no está instalado."
    echo "        Instálalo desde: https://www.python.org/downloads/"
    exit 1
fi

echo "[INFO] Usando: $($PYTHON_CMD --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "[INFO] Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    echo "[OK] Entorno virtual creado"
else
    echo "[OK] Entorno virtual encontrado"
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "[INFO] Instalando dependencias..."
pip install -r requerimientos.txt --quiet
echo "[OK] Dependencias instaladas"

echo ""
echo "=================================================="
echo " Iniciando servidor PrivaScanner..."
echo "   URL: http://localhost:8000"
echo "   Presiona Ctrl+C para detener"
echo "=================================================="
echo ""

# Iniciar servidor
uvicorn PrivaScanner:app --reload
