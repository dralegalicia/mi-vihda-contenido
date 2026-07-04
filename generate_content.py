import os
import google.generativeai as genai
import json

# 1. Configuración de la llave
# GitHub tomará automáticamente la clave de tus "Secrets"
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def obtener_mejor_modelo():
    """Busca automáticamente el modelo disponible en tu cuenta"""
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

prompt = """
Actúa como un psicólogo clínico y nutriólogo experto en VIH y Obesidad. 
Genera contenido dinámico para una app de salud en Río Blanco, Veracruz, con tono empático y libre de estigma.
Genera exactamente: 2 noticias, 1 consejo de nutrición, 1 receta saludable, 1 recurso de obesidad y el bloque de SALUD MENTAL.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura exacta, sin marcas de código (no uses ```json):
{
  "recursos_obesidad": [
    {
      "id": 1, 
      "titulo": "Título del recurso", 
      "descripcion": "Descripción breve", 
      "link": "Link real de salud (ej. gob.mx o mayoclinic)"
    }
  ],
  "noticias": [
    {
      "id": 1, 
      "titulo": "Título noticia", 
      "resumen": "Resumen breve", 
      "url_imagen": "URL de imagen real de Unsplash", 
      "link": "Link a noticia real"
    }
  ],
  "consejos": [
    {
      "id": 1, 
      "titulo": "Título consejo", 
      "texto": "Texto del consejo"
    }
  ],
  "recetas": [
    {
      "id": 1, 
      "nombre": "Nombre receta", 
      "url_imagen": "URL de imagen de comida de Unsplash", 
      "descripcion": "Breve descripción", 
      "link_externo": "Link a kiwilimon o similar"
    }
  ],
  "salud_mental": {
      "emocion_del_dia": "Frase breve para reflexionar sobre el ánimo hoy.",
      "desafio": "Acción sencilla de autocuidado (ej. respirar, caminar, agradecer).",
      "afirmacion_positiva": "Afirmación potente para reducir estrés del tratamiento.",
      "puntos_ganados": 50
  }
}
"""

try:
    nombre_modelo = obtener_mejor_modelo()
    print(f"Usando modelo: {nombre_modelo}")
    model = genai.GenerativeModel(nombre_modelo)
    response = model.generate_content(prompt)
    
    texto = response.text.strip()
    # Limpieza de seguridad para extraer el JSON puro
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    json_puro = texto[inicio:fin]
    
    # Validar que es un JSON correcto antes de guardar
    datos = json.loads(json_puro)
    
    # Guardar el archivo final
    with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("¡Éxito! Contenido integral (Nutrición + Salud Mental) actualizado.")

except Exception as e:
    print(f"Error al generar contenido: {e}")
    exit(1)
