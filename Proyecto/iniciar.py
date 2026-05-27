#!/usr/bin/env python3
"""
PrivaScanner - Script de inicio multiplataforma.
Funciona en Windows, macOS y Linux.

Uso: python iniciar.py
"""

import os
import sys
import subprocess
import platform


def obtener_directorio_backend():
    """Obtiene la ruta absoluta al directorio backend."""
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio_script, "backend")


def obtener_rutas_venv(directorio_backend):
    """Obtiene las rutas del virtualenv según el sistema operativo."""
    venv_dir = os.path.join(directorio_backend, "venv")

    if os.name == "nt":  # Windows
        python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
    else:  # macOS / Linux
        python_bin = os.path.join(venv_dir, "bin", "python")

    return venv_dir, python_bin


def verificar_python():
    """Verifica que Python 3 esté disponible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] Se requiere Python 3.8 o superior.")
        print(f"        Versión actual: {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro} detectado")


def crear_virtualenv(venv_dir, python_bin):
    """Crea el entorno virtual si no existe o está incompleto."""
    if os.path.exists(venv_dir):
        if os.path.exists(python_bin):
            print("[OK] Entorno virtual encontrado")
            return
        else:
            # El venv existe pero está corrupto/incompleto, recrear
            print("[WARN] Entorno virtual incompleto detectado, recreando...")
            import shutil
            shutil.rmtree(venv_dir)

    print("[INFO] Creando entorno virtual...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print("[OK] Entorno virtual creado correctamente")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al crear el entorno virtual: {e}")
        sys.exit(1)


def instalar_dependencias(python_bin, directorio_backend):
    """Instala las dependencias del proyecto usando python -m pip."""
    requerimientos = os.path.join(directorio_backend, "requerimientos.txt")

    if not os.path.exists(requerimientos):
        print("[ERROR] No se encontró el archivo requerimientos.txt")
        sys.exit(1)

    print("[INFO] Instalando dependencias...")
    try:
        subprocess.check_call(
            [python_bin, "-m", "pip", "install", "-r", requerimientos, "--quiet"],
        )
        print("[OK] Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al instalar dependencias: {e}")
        print("        Intenta ejecutar manualmente:")
        print(f"        {python_bin} -m pip install -r {requerimientos}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el ejecutable de Python en: {python_bin}")
        print("        Intenta eliminar la carpeta backend/venv y ejecutar de nuevo.")
        sys.exit(1)


def iniciar_servidor(python_bin, directorio_backend):
    """Inicia el servidor uvicorn."""
    print()
    print("=" * 50)
    print(" Iniciando servidor PrivaScanner...")
    print(" URL: http://localhost:8000")
    print(" Presiona Ctrl+C para detener")
    print("=" * 50)
    print()

    try:
        subprocess.check_call(
            [python_bin, "-m", "uvicorn", "PrivaScanner:app", "--reload"],
            cwd=directorio_backend,
        )
    except KeyboardInterrupt:
        print("\n\n[INFO] Servidor detenido por el usuario.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Error al iniciar el servidor: {e}")
        sys.exit(1)


def main():
    sistema = platform.system()
    print()
    print("==================================================")
    print(" PrivaScanner v1.0")
    print(f" Sistema detectado: {sistema}")
    print("==================================================")
    print()

    verificar_python()

    directorio_backend = obtener_directorio_backend()

    if not os.path.exists(directorio_backend):
        print(f"[ERROR] No se encontró el directorio backend en: {directorio_backend}")
        sys.exit(1)

    venv_dir, python_bin = obtener_rutas_venv(directorio_backend)

    crear_virtualenv(venv_dir, python_bin)
    instalar_dependencias(python_bin, directorio_backend)
    iniciar_servidor(python_bin, directorio_backend)


if __name__ == "__main__":
    main()
