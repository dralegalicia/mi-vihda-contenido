import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Lista de Videos de YouTube (Verificados que funcionan al 100%)
YOUTUBE_RECETAS = [
    "https://www.youtube.com/watch?v=DOfV8E7T3yE", # Pescado empapelado
    "https://www.youtube.com/watch?v=0hYw_zL8U6M", # Ensalada nutritiva
    "https://www.youtube.com/watch?v=NnF_6zE5mYo", # Pollo con verduras
    "https://www.youtube.com/watch?v=fB3AAm98CNo"  # Desayuno saludable
]

YOUTUBE_OBESIDAD = [
    "https://www.youtube.com/watch?v=Z_a7zNOnf5s", # Ejercicios en casa
    "https://www.youtube.com/watch?v=0vT_Wv72m2I"  # Consejos contra obesidad
]

def obtener_mejor_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name: return m.name
    except: pass
    return 'gemini-pro'

prompt = f"""
Actúa como un psicólogo y nutriólogo experto en VIH. 
Genera contenido dinámico para una app de salud en México.

REGLA DE ORO PARA LINKS DE VIDEO:
- Para 'link_externo' de recetas, usa SOLO uno de estos: {YOUTUBE_RECETAS}
- Para 'link' de obesidad, usa SOLO uno de estos: {YOUTUBE_OBESIDAD}
- Para 'link' de noticias, usa 'https://news.un.org/es/tags/salud'

Genera exactamente: 1 noticia, 1 consejo, 1 receta, 1 recurso de obesidad y salud_mental.
Usa fotos de stock de Unsplash que se vean ricas y saludables.

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
    
    print("¡ÉXITO! Contenido con videos de YouTube generado.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
