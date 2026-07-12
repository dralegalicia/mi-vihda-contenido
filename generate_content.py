import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# 1. Configuración de API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY no configurada.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt, fallback):
    try:
        response = model.generate_content(prompt + ". Responde directamente en español, breve.")
        return response.text.strip() if response.text else fallback
    except:
        return fallback

def generar_mito_trivia():
    temas = ["VIH", "Riesgo Cardiovascular", "Psicología", "PrEP", "DoxiPrEP", "Hipertensión", "Diabetes"]
    tema = random.choice(temas)
    prompt = f"Genera un mito de salud sobre {tema}. Responde SOLO un JSON: {{\"tema\":\"{tema}\", \"mito\":\"...\", \"realidad\":\"...\", \"pregunta\":\"...\", \"opciones\":[\"A\",\"B\",\"C\"], \"respuesta_correcta\":0, \"explicacion_ia\":\"...\"}}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "{" in text: text = text[text.find("{"):text.rfind("}")+1]
        return json.loads(text)
    except: return None

# 2. Biblioteca de Videos (Canales solicitados)
VIDEOS = [
    {"n": "Ensalada de Lentejas - Kiwilimón", "v": "https://www.youtube.com/watch?v=L_TfW0q_o0o"},
    {"n": "Pollo a la Jardinera - Cocina de Addy", "v": "https://www.youtube.com/watch?v=7Mh1Bih_m2o"},
    {"n": "Pescado al Vapor - Chef Oropeza", "v": "https://www.youtube.com/watch?v=F_YF-9H0b90"},
    {"n": "Sopa de Verduras - Kiwilimón", "v": "https://www.youtube.com/watch?v=7M5_V0I9m68"}
]
vid = random.choice(VIDEOS)

# 3. Generar CONTENIDO NUTRI (Con bienvenida original)
nutri_data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Usa la calculadora de IMC y Grasa para que el robot pueda darte mejores consejos de salud.",
        "activo": True
    },
    "noticias": [{"id":1, "titulo":"Salud Hoy", "resumen": generar_texto("Noticia salud VIH positiva", "Cuidar tu salud es vivir mejor."), "url_imagen":"https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800", "link":"https://news.un.org/es/tags/salud"}],
    "consejos": [{"id":1, "titulo":"Tip Nutri", "texto": generar_texto("Consejo nutrición VIH", "Hidrátate bien todos los días.")}],
    "recetas": [{"id":1, "nombre": vid["n"], "url_imagen":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800", "descripcion": "Receta saludable recomendada.", "link_externo": vid["v"]}],
    "salud_mental": {"emocion_del_dia":"Paz", "desafio":"Respira hondo.", "afirmacion_positiva":"Soy salud.", "puntos_ganados":50}
}

# 4. Generar SALUD (Mitos)
salud_data = { "mito_del_dia": generar_mito_trivia() }

# 5. Guardar archivos
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)
with open('salud.json', 'w', encoding='utf-8') as f:
    json.dump(salud_data, f, ensure_ascii=False, indent=2)

print("¡Archivos generados: contenido_nutri.json y salud.json!")
