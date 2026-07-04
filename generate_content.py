import os
import google.generativeai as genai
import json
import random

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Lista de Enlaces Reales y Verificados (Copia y pega tal cual)
LINKS_RECETAS = [
    "https://www.kiwilimon.com/recetas/saludables/recetas-con-pollo-saludables",
    "https://www.kiwilimon.com/recetas/saludables/cenas-saludables",
    "https://www.dietdoctor.com/es/recetas/cenas",
    "https://www.cocinafacil.com.mx/recetas/recetas-saludables"
]

LINKS_NOTICIAS = [
    "https://news.un.org/es/tags/salud",
    "https://www.mayoclinic.org/es/diseases-conditions/hiv-aids/symptoms-causes/syc-20373524",
    "https://www.who.int/es/news-room/fact-sheets/detail/hiv-aids"
]

def obtener_mejor_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name: return m.name
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
    except: pass
    return 'gemini-pro'

prompt = f"""
Actúa como un psicólogo y nutriólogo experto en VIH. 
Genera contenido dinámico para una app de salud en México.

REGLA OBLIGATORIA PARA LOS LINKS:
- Para 'link_externo' de recetas, elige UNO de estos: {LINKS_RECETAS}
- Para 'link' de noticias, elige UNO de estos: {LINKS_NOTICIAS}
- Para 'link' de obesidad, usa siempre: 'https://www.who.int/es/news-room/fact-sheets/detail/obesity-and-overweight'

Genera exactamente: 2 noticias, 1 consejo, 1 receta, 1 recurso de obesidad y salud_mental.
Usa fotos de stock de Unsplash relacionadas con el tema.

IMPORTANTE: Devuelve ÚNICAMENTE el objeto JSON puro sin marcas de código:
{{
  "recursos_obesidad": [{{ "id": 1, "titulo": "...", "descripcion": "...", "link": "..." }}],
  "noticias": [{{ "id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..." }}],
  "consejos": [{{ "id": 1, "titulo": "...", "texto": "..." }}],
  "recetas": [{{ "id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..." }}],
  "salud_mental": {{ "emocion_del_dia": "...", "desafio": "...", "afirmacion_positiva": "...", "puntos_ganados": 50 }}
}}
"""

try:
    nombre_modelo = obtener_mejor_modelo()
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_final = texto[inicio:fin]
    
    datos = json.loads(json_final)
    
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡Contenido con links verificados generado!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
