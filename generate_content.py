import os
import json
import requests

def generar_con_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    # URL directa del servidor de Google (Versión estable 1.5 Flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt = """
    Actúa como un nutriólogo experto en VIH. Genera contenido para una app en México.
    IMPORTANTE: Usa links REALES de kiwilimon.com, cookpad.com o mayoclinic.org.
    Genera exactamente: 2 noticias, 2 consejos, 2 recetas y 2 recursos de obesidad.
    Usa fotos reales de Unsplash o Pexels.
    
    Devuelve ÚNICAMENTE el objeto JSON sin marcas de código:
    {
      "recursos_obesidad": [{"id": 1, "titulo": "...", "descripcion": "...", "link": "..."}],
      "noticias": [{"id": 1, "titulo": "...", "resumen": "...", "url_imagen": "...", "link": "..."}],
      "consejos": [{"id": 1, "titulo": "...", "texto": "..."}],
      "recetas": [{"id": 1, "nombre": "...", "url_imagen": "...", "descripcion": "...", "link_externo": "..."}]
    }
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        res_json = response.json()
        
        # Extraer el texto de la respuesta de Google
        texto = res_json['candidates'][0]['content']['parts'][0]['text']
        
        # Limpiar el texto para obtener solo el JSON
        inicio = texto.find("{")
        fin = texto.rfind("}") + 1
        json_final = texto[inicio:fin]
        
        # Validar que es un JSON correcto
        datos = json.loads(json_final)
        
        with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
            
        print("¡LOGRADO! Archivo actualizado correctamente.")
        return True
    except Exception as e:
        print(f"Error en la conexión directa: {e}")
        return False

if __name__ == "__main__":
    if not generar_con_gemini():
        exit(1)
