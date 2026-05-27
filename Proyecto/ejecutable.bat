@echo off
echo.
echo ======================================
echo         PrivaScanner v1.0
echo         Sistema: Windows
echo ======================================
echo.

:: Verificar que Python esté instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado.
    echo         Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

cd backend

:: Crear entorno virtual si no existe
if not exist venv (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [OK] Entorno virtual encontrado
)

:: Activar entorno virtual
call venv\Scripts\activate.bat

:: Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requerimientos.txt --quiet
echo [OK] Dependencias instaladas

echo.
echo ==================================================
echo    Iniciando servidor PrivaScanner...
echo    URL: http://localhost:8000
echo    Presiona Ctrl+C para detener
echo ==================================================
echo.

:: Iniciar servidor
uvicorn PrivaScanner:app --reload
