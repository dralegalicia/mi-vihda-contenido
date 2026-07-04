import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def obtener_mejor_modelo():
    print("Buscando modelos disponibles en tu cuenta...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Preferimos el 1.5 flash, pero si no está, usamos cualquiera que sirva
                if 'gemini-1.5-flash' in m.name:
                    print(f"Usando modelo preferido: {m.name}")
                    return m.name
        # Si no encontró el preferido, toma el primero que genere contenido
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Usando modelo alternativo encontrado: {m.name}")
                return m.name
    except Exception as e:
        print(f"Error al listar modelos: {e}")
    return 'gemini-pro' # Fallback final

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad. 
Genera contenido dinámico para una app de salud en Río Blanco, Veracruz.
Genera exactamente: 2 noticias, 2 consejos, 2 recetas y 2 recursos de obesidad.
IMPORTANTE: Devuelve ÚNICAMENTE el objeto JSON sin texto extra:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
Usa fotos de stock reales (Pexels/Freepik) y links oficiales de salud.
"""

try:
    nombre_modelo = obtener_mejor_modelo()
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    # Extraer el JSON puro entre las llaves { }
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_puro = texto[inicio:fin]
    
    # Validar que es un JSON correcto
    datos = json.loads(json_puro)
    
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡PROCESO COMPLETADO CON ÉXITO!")

except Exception as e:
    print(f"Error final: {e}")
    exit(1)
