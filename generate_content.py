import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def obtener_mejor_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return m.name
    except:
        pass
    return 'gemini-pro'

prompt = """
Actúa como un nutriólogo clínico experto en VIH. 
Genera contenido dinámico para una app de salud en México.
IMPORTANTE: Para los enlaces (links), utiliza ÚNICAMENTE estos sitios web reales y seguros:
- Recetas: kiwilimon.com, cookpad.com, o dietdoctor.com/es/recetas
- Noticias/Recursos: mayoclinic.org, medlineplus.gov/spanish, o gob.mx/salud

Genera exactamente: 2 noticias, 2 consejos, 2 recetas y 2 recursos de obesidad.
Para las imágenes (url_imagen), usa URLs reales de Unsplash o Pexels que terminen en .jpg o .png.

Devuelve ÚNICAMENTE el objeto JSON sin texto extra:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
"""

try:
    nombre_modelo = obtener_mejor_modelo()
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_puro = texto[inicio:fin]
    
    datos = json.loads(json_puro)
    
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡Contenido actualizado con links reales!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
