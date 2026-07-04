import os
import json
import requests

def generar_con_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Probaremos con la URL de producción más estable que existe
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt = """
    Actúa como un nutriólogo experto en VIH. Genera contenido para una app de salud en México.
    IMPORTANTE: Usa links REALES que funcionen de: kiwilimon.com o mayoclinic.org.
    Genera exactamente: 2 noticias, 2 consejos, 2 recetas y 2 recursos de obesidad.
    Usa fotos reales de Unsplash.
    
    Devuelve ÚNICAMENTE un objeto JSON sin marcas de código ni texto extra:
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
        print("Conectando con el servidor estable de Google...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"La versión v1 falló, intentando v1beta como plan B...")
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(url_alt, headers=headers, json=payload)

        response.raise_for_status()
        res_json = response.json()
        
        texto = res_json['candidates'][0]['content']['parts'][0]['text']
        
        # Limpiar el texto para obtener solo el JSON
        inicio = texto.find("{")
        fin = texto.rfind("}") + 1
        json_final = texto[inicio:fin]
        
        datos = json.loads(json_final)
        
        with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
            
        print("¡POR FIN! Contenido generado y guardado.")
        return True
    except Exception as e:
        print(f"Error persistente: {e}")
        return False

if __name__ == "__main__":
    if not generar_con_gemini():
        exit(1)
