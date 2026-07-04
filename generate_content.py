import os
import google.generativeai as genai
import json

# Configurar la IA (La clave se tomará de GitHub Secrets)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad para el CAPASITS Río Blanco, Veracruz. 
Genera contenido dinámico para una app de salud. 
El tono debe ser cálido, empático y profesional.
Genera exactamente:
- 2 noticias recientes de salud relacionadas con nutrición o VIH.
- 2 consejos prácticos de nutrición.
- 2 recetas saludables (incluye una URL de imagen de stock de comida).
- 2 recursos con links sobre prevención de obesidad.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura exacta:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
"""

try:
    response = model.generate_content(prompt)
    # Limpieza de la respuesta para obtener solo el JSON
    content = response.text.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    # Validar que sea un JSON válido antes de guardar
    json.loads(content)

    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Archivo actualizado con éxito.")
except Exception as e:
    print(f"Error al generar contenido: {e}")
    exit(1)
