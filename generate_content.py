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

# 2. Mitos de Respaldo (Si la IA falla, usará uno de estos)
MITOS_REPALDO = [
    {
        "tema": "VIH",
        "mito": "El VIH se transmite por compartir cubiertos o besos.",
        "realidad": "Falso. El VIH no se transmite por saliva, sudor o contacto casual.",
        "pregunta": "¿Cuál es una vía real de transmisión del VIH?",
        "opciones": ["Contacto con sangre infectada", "Picadura de mosquito", "Abrazos"],
        "respuesta_correcta": 0,
        "explicacion_ia": "¡Excelente! Conocer las vías reales de transmisión elimina el estigma y nos protege a todos."
    },
    {
        "tema": "Diabetes",
        "mito": "Comer mucha azúcar es la única causa de la diabetes.",
        "realidad": "La diabetes es multifactorial, incluye genética, estilo de vida y peso.",
        "pregunta": "¿Qué factor influye en el desarrollo de diabetes tipo 2?",
        "opciones": ["Genética y obesidad", "Solo comer dulces", "Usar lentes"],
        "respuesta_correcta": 0,
        "explicacion_ia": "¡Correcto! Una vida equilibrada es nuestra mejor defensa."
    }
]

def generar_mito_trivia():
    temas = ["VIH", "Riesgo Cardiovascular", "Psicología", "PrEP", "DoxiPrEP", "Hipertensión", "Diabetes"]
    tema = random.choice(temas)
    
    prompt = f"""
    Actúa como un médico experto. Genera un mito de salud sobre {tema} en México.
    Responde UNICAMENTE un objeto JSON puro (sin bloques de código) con estas llaves:
    "tema", "mito", "realidad", "pregunta", "opciones" (lista de 3), "respuesta_correcta" (0, 1 o 2), "explicacion_ia".
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Limpieza profunda por si la IA agrega texto extra
        if "{" in text:
            text = text[text.find("{"):text.rfind("}")+1]
        return json.loads(text)
    except Exception as e:
        print(f"La IA no pudo generar el mito ({e}). Usando respaldo.")
        return random.choice(MITOS_REPALDO)

# 3. Generar archivos
vid = random.choice([
    {"n": "Ensalada de Lentejas - Kiwilimón", "v": "https://www.youtube.com/watch?v=L_TfW0q_o0o"},
    {"n": "Pollo a la Jardinera - Cocina de Addy", "v": "https://www.youtube.com/watch?v=7Mh1Bih_m2o"}
])

nutri_data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Usa la calculadora de IMC y Grasa para que el robot pueda darte mejores consejos de salud.",
        "activo": True
    },
    "noticias": [{"id":1, "titulo":"Salud Hoy", "resumen": "Cuidar tu salud es vivir mejor.", "url_imagen":"https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800", "link":"https://news.un.org/es/tags/salud"}],
    "consejos": [{"id":1, "titulo":"Tip Nutri", "texto": "Bebe al menos 2 litros de agua al día."}],
    "recetas": [{"id":1, "nombre": vid["n"], "url_imagen":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800", "descripcion": "Receta saludable recomendada.", "link_externo": vid["v"]}],
    "salud_mental": {"emocion_del_dia":"Paz", "desafio":"Respira hondo.", "afirmacion_positiva":"Soy salud.", "puntos_ganados":50}
}

salud_data = { "mito_del_dia": generar_mito_trivia() }

# 4. Guardar
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)
with open('salud.json', 'w', encoding='utf-8') as f:
    json.dump(salud_data, f, ensure_ascii=False, indent=2)

print("Archivos actualizados correctamente.")
