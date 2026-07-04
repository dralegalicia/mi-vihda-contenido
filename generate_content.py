import os
import json
from google import genai

# Usar el nuevo cliente oficial de Google
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad para el CAPASITS Río Blanco, Veracruz. 
Genera contenido dinámico para una app de salud. El tono debe ser cálido, empático y profesional.
Genera exactamente:
- 2 noticias recientes de salud.
- 2 consejos prácticos de nutrición.
- 2 recetas saludables (usa URLs de imágenes de stock de comida de pexels o freepik).
- 2 recursos con links oficiales sobre prevención de obesidad.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura exacta, sin marcas de código:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
"""

try:
    # Llamar al modelo flash (el más rápido y estable)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    
    content = response.text.strip()
    
    # Limpieza de seguridad por si la IA agrega texto extra
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]

    parsed_json = json.loads(content)

    # Guardar el archivo JSON
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        
    print("Contenido generado exitosamente con la nueva librería.")

except Exception as e:
    print(f"Error detectado: {e}")
    exit(1)
