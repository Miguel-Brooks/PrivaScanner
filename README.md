# PrivaScanner

Extensión de Chrome que analiza automáticamente los **Términos y Condiciones** y **Políticas de Privacidad** de cualquier sitio web usando inteligencia artificial (Google Gemini).

## Requisitos

- **Python 3.8+** — [Descargar](https://www.python.org/downloads/)
- **Google Chrome** — Para la extensión
- **API Key de Gemini** — [Obtener gratis](https://aistudio.google.com/apikey)

## Configuración

### 1. Configurar la API Key

```bash
# Copia el archivo de ejemplo
cp backend/.env.example backend/.env

# Edita backend/.env y reemplaza con tu API key real
# GEMINI_API_KEY=tu_api_key_aqui
```

### 2. Iniciar el servidor

#### Opción recomendada — Script Python (funciona en todos los sistemas)

```bash
python iniciar.py
```

#### macOS / Linux — Script Shell

```bash
chmod +x iniciar.sh
./iniciar.sh
```

#### Windows — Script Batch

```cmd
ejecutable.bat
```

El servidor se iniciará en `http://localhost:8000`.

### 3. Instalar la extensión en Chrome

1. Abre Chrome y ve a `chrome://extensions/`
2. Activa el **Modo de desarrollador** (esquina superior derecha)
3. Haz clic en **"Cargar extensión sin empaquetar"**
4. Selecciona la carpeta `extension/`

## Uso

1. Asegúrate de que el servidor esté corriendo (`python iniciar.py`)
2. Navega a cualquier página con Términos y Condiciones o Política de Privacidad
3. PrivaScanner detectará automáticamente el contenido legal y mostrará un panel con el análisis

El panel muestra:
- **Datos Recopilados** — Qué información tuya recopila el sitio
- **Permisos Críticos** — Accesos importantes que estás otorgando
- **Alertas y Riesgos** — Cláusulas que podrían afectarte

## Estructura del Proyecto

```
Proyecto/
├── iniciar.py              # Script principal (multiplataforma)
├── iniciar.sh              # Script para macOS/Linux
├── ejecutable.bat          # Script para Windows
├── README.md
├── .gitignore
├── backend/
│   ├── PrivaScanner.py     # API FastAPI + Gemini
│   ├── requerimientos.txt  # Dependencias Python
│   ├── .env.example        # Template de configuración
│   └── .env                # Tu configuración (no se sube al repo)
└── extension/
    ├── manifest.json       # Configuración de la extensión
    ├── background.js       # Service worker
    ├── contenido.js        # Content script
    └── estilos.css         # Estilos del panel
```

## Seguridad

- **Nunca subas tu archivo `.env`** al repositorio — está incluido en `.gitignore`
- La API key se carga desde variables de entorno, no del código fuente
