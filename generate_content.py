import os
import google.generativeai as genai
import json

# Configurar la IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Usamos el modelo flash 1.5 que es el más estable actualmente
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad para el CAPASITS Río Blanco, Veracruz. 
Genera contenido dinámico para una app de salud. 
El tono debe ser cálido, empático y profesional.
Genera exactamente:
- 2 noticias recientes de salud.
- 2 consejos prácticos de nutrición.
- 2 recetas saludables (usa URLs de imágenes de stock de comida de pexels o freepik).
- 2 recursos con links oficiales sobre obesidad.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura exacta, sin marcas de código:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "description": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
"""

try:
    response = model.generate_content(prompt)
    content = response.text.strip()
    
    # Limpiar si la IA agrega texto extra
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]

    parsed_json = json.loads(content)

    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        
    print("Contenido generado con éxito.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
