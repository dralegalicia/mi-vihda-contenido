import os
import google.generativeai as genai
import json

# Configurar la llave
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Usamos el nombre técnico del modelo que es más compatible
model = genai.GenerativeModel('models/gemini-1.5-flash')

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad para el CAPASITS Río Blanco, Veracruz. 
Genera contenido dinámico para una app de salud. El tono debe ser cálido, empático y profesional.
Genera exactamente:
- 2 noticias recientes de salud.
- 2 consejos prácticos de nutrición.
- 2 recetas saludables (usa URLs de imágenes de comida de pexels o freepik).
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
    # Generar contenido
    response = model.generate_content(prompt)
    content = response.text.strip()
    
    # Limpieza extrema del JSON
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]

    # Validar JSON
    parsed_json = json.loads(content)

    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        
    print("¡Éxito! Contenido generado.")

except Exception as e:
    print(f"Error: {e}")
    # Si falla, intentamos con el modelo alternativo
    try:
        model_alt = genai.GenerativeModel('gemini-pro')
        response = model_alt.generate_content(prompt)
        # (Lógica de guardado simplificada)
        content = response.text.strip()
        if "{" in content: content = content[content.find("{"):content.rfind("}")+1]
        with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        exit(1)
