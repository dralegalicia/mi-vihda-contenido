import os
import google.generativeai as genai
import json
import time

# 1. Configurar la llave
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Lista de modelos a probar (Google ha cambiado los nombres recientemente)
# Intentaremos con todos estos hasta que uno acepte la petición
modelos_a_probar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']

prompt = """
Actúa como un nutriólogo clínico experto en VIH y Obesidad. 
Genera contenido dinámico para una app de salud en Río Blanco, Veracruz.
Genera exactamente: 2 noticias, 2 consejos, 2 recetas y 2 recursos de obesidad.
IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON con esta estructura:
{
  "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
  "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
  "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
  "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
}
Usa links reales de salud y fotos de comida de pexels o freepik.
"""

def ejecutar_actualizacion():
    for nombre in modelos_a_probar:
        try:
            print(f"Intentando con el modelo: {nombre}...")
            model = genai.GenerativeModel(nombre)
            response = model.generate_content(prompt)
            
            texto = response.text.strip()
            # Limpiar el texto para quedarnos solo con el JSON { ... }
            inicio = texto.find("{")
            fin = texto.rfind("}") + 1
            json_final = texto[inicio:fin]
            
            # Validar que sea un JSON real
            datos = json.loads(json_final)
            
            with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            print(f"¡ÉXITO TOTAL con el modelo {nombre}!")
            return True
        except Exception as e:
            print(f"El modelo {nombre} falló: {e}")
            time.sleep(2) # Esperar un poco antes de intentar el siguiente
    return False

if __name__ == "__main__":
    if not ejecutar_actualizacion():
        print("No se pudo generar contenido con ningún modelo disponible.")
        exit(1)
