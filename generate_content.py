import os
import google.generativeai as genai
import json

# Configurar la IA (La clave se tomará de GitHub Secrets)
# Usamos gemini-1.5-flash que es el modelo actual gratuito y rápido
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad para el CAPASITS Río Blanco, Veracruz. 
Genera contenido dinámico para una app de salud. 
El tono debe ser cálido, empático y profesional.
Genera exactamente:
- 2 noticias recientes de salud relacionadas con nutrición o VIH.
- 2 consejos prácticos de nutrición.
- 2 recetas saludables (incluye una URL de imagen de stock de comida real de pexels o freepik).
- 2 recursos con links oficiales (gob.mx o instituciones de salud) sobre prevención de obesidad.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura exacta, sin texto adicional antes o después:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
"""

try:
    response = model.generate_content(prompt)
    content = response.text.strip()
    
    # Limpieza robusta del JSON por si la IA pone marcas de código
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]

    # Validar que sea un JSON válido antes de guardar
    parsed_json = json.loads(content)

    # Guardar con formato para que sea legible
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        
    print("¡Contenido generado y archivo actualizado con éxito!")
except Exception as e:
    print(f"Error crítico al generar contenido: {e}")
    exit(1)
