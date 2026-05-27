import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv(Path(__file__).parent / ".env")

app = FastAPI()

# Configurar CORS para permitir peticiones desde la extensión
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar API Key desde variables de entorno
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("[WARN] No se encontró GEMINI_API_KEY.")
    print("   Copia backend/.env.example a backend/.env y configura tu API key.")
else:
    genai.configure(api_key=api_key)

class AnalisisRequest(BaseModel):
    texto: str

@app.post("/analizar")
async def analizar_texto(request: AnalisisRequest):
    try:
        # Se leeran hasta 50,000 caracteres de texto
        texto = request.texto[:50000] 

        # Modelo de IA que se utilizara
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        Analiza los siguientes Términos y Condiciones o Política de Privacidad.
        Extrae la información más importante para el usuario y devuélvela ESTRICTAMENTE en este formato Markdown:
        
        ### Datos Recopilados
        [Lista de datos que la plataforma recopila del usuario]
        
        ### Permisos Críticos
        [Lista de permisos importantes a los que el usuario está accediendo, ejemplo: ubicación, cámara, compartir datos con terceros, microfono, contactos, etc.]
        
        ### Alertas y Riesgos
        [Lista de cláusulas abusivas, renuncias de responsabilidad o riesgos para la privacidad, todo lo que pueda afectar al usuario]
        
        Texto a analizar:
        {texto}
        """
        
        response = model.generate_content(prompt)
        return {"resultado": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
