import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def obtener_mejor_modelo():
    print("Detectando qué modelo tienes activo en Google...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    print(f"Modelo encontrado: {m.name}")
                    return m.name
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        pass
    return 'gemini-pro'

prompt = """
Actúa como un psicólogo y nutriólogo experto en VIH. 
Genera contenido dinámico para una app de salud en México con tono empático.

IMPORTANTE PARA LOS ENLACES (Síguelas estrictamente):
- Recetas: Solo usa links reales de 'https://www.dietdoctor.com/es/recetas' o 'https://www.cocinafacil.com.mx/recetas'.
- Noticias: Solo usa links reales de 'https://news.un.org/es/tags/salud' o 'https://www.mayoclinic.org/es/diseases-conditions/hiv-aids/symptoms-causes/syc-20373524'.
- Obesidad: Solo usa 'https://www.who.int/es/news-room/fact-sheets/detail/obesity-and-overweight'.

Genera exactamente: 2 noticias, 1 consejo, 1 receta, 1 recurso de obesidad y el bloque salud_mental.
Usa fotos de stock de Unsplash (fotos de comida real).

IMPORTANTE: Devuelve ÚNICAMENTE el objeto JSON sin marcas de código:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}],
  "salud_mental": {"emocion_del_dia": "...", "desafio": "...", "afirmacion_positiva": "...", "puntos_ganados": 50}
}
"""

try:
    nombre_modelo = obtener_mejor_modelo()
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    # Limpieza de seguridad para extraer el JSON
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_puro = texto[inicio:fin]
    
    datos = json.loads(json_puro)
    
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡TODO LISTO! Contenido actualizado con éxito.")

except Exception as e:
    print(f"Falla: {e}")
    exit(1)
