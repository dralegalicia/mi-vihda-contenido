import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Lista de Videos de YouTube Reales
YOUTUBE_RECETAS = [
    "https://www.youtube.com/watch?v=DOfV8E7T3yE",
    "https://www.youtube.com/watch?v=0hYw_zL8U6M",
    "https://www.youtube.com/watch?v=NnF_6zE5mYo"
]

YOUTUBE_OBESIDAD = [
    "https://www.youtube.com/watch?v=Z_a7zNOnf5s",
    "https://www.youtube.com/watch?v=0vT_Wv72m2I"
]

def obtener_mejor_modelo():
    """Busca qué modelo tienes permitido usar en tu cuenta"""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        pass
    return 'gemini-pro'

prompt = f"""
Actúa como un psicólogo y nutriólogo experto en VIH. 
Genera contenido dinámico para una app de salud en México con tono empático.

REGLA DE ORO PARA LINKS DE VIDEO:
- Para 'link_externo' de recetas, usa SOLO uno de estos: {YOUTUBE_RECETAS}
- Para 'link' de recursos de obesidad, usa SOLO uno de estos: {YOUTUBE_OBESIDAD}
- Para 'link' de noticias, usa siempre: 'https://news.un.org/es/tags/salud'

Genera exactamente: 1 noticia, 1 consejo, 1 receta, 1 recurso de obesidad y el bloque salud_mental.
Usa fotos de stock de Unsplash (fotos de comida real).

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
    # Autodetección de modelo
    nombre_modelo = obtener_mejor_modelo()
    print(f"Usando modelo detectado: {nombre_modelo}")
    
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    # Limpieza para extraer el JSON
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_final = texto[inicio:fin]
    
    datos = json.loads(json_final)
    
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡TODO LISTO! Contenido actualizado con éxito.")

except Exception as e:
    print(f"Falla: {e}")
    exit(1)
