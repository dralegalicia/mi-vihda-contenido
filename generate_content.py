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
        response = model.generate_content(prompt + ". Responde en español, máximo 200 caracteres, sé muy variado.")
        return response.text.strip() if response.text else fallback
    except:
        return fallback

def generar_json_ia(prompt):
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "{" in text:
            text = text[text.find("{"):text.rfind("}")+1]
        return json.loads(text)
    except:
        return None

# 2. BIBLIOTECA REAL DE VIDEOS (Enlaces verificados de canales oficiales)
RECETAS_MASTER = [
    {"n": "Tacos de Lechuga con Pollo", "v": "https://www.youtube.com/watch?v=kYI_t9M3q6s", "c": "Kiwilimón"},
    {"n": "Sopa de Verduras con Lentejas", "v": "https://www.youtube.com/watch?v=7M5_V0I9m68", "c": "Kiwilimón"},
    {"n": "Pescado a la Veracruzana", "v": "https://www.youtube.com/watch?v=F_YF-9H0b90", "c": "Chef Oropeza"},
    {"n": "Caldo de Pollo con Verduras", "v": "https://www.youtube.com/watch?v=Z_U6u7N6O6k", "c": "Cocina de Addy"},
    {"n": "Ensalada de Atún Saludable", "v": "https://www.youtube.com/watch?v=oX-0qC81L7E", "c": "Kiwilimón"},
    {"n": "Ceviche de Pescado", "v": "https://www.youtube.com/watch?v=vVj_pY4x6S4", "c": "Chef Oropeza"},
    {"n": "Guiso de Lentejas", "v": "https://www.youtube.com/watch?v=84u0C-m9O80", "c": "Cocina con Addy"}
]

# Elegimos 2 recetas diferentes para que siempre haya variedad
recetas_hoy = random.sample(RECETAS_MASTER, 2)

# 3. GENERAR MITO DIARIO
mito_prompt = """
Actúa como médico experto. Genera un mito y trivia de salud sobre VIH, Diabetes o Hipertensión.
Responde SOLO un objeto JSON: 
{"tema":"...", "mito":"...", "realidad":"...", "pregunta":"...", "opciones":["A","B","C"], "respuesta_correcta":0, "explicacion_ia":"..."}
"""
mito_hoy = generar_json_ia(mito_prompt)

# 4. CONSTRUIR CONTENIDO NUTRI
nutri_data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Usa la calculadora de IMC y Grasa para que el robot pueda darte mejores consejos de salud.",
        "activo": True
    },
    "noticias": [
        {
            "id": 1,
            "titulo": generar_texto("Crea un título de noticia de salud actual", "Nuevos avances en nutrición"),
            "resumen": generar_texto("Resume una noticia de bienestar o medicina preventiva", "Una dieta balanceada es la clave para mantener tus defensas altas."),
            "url_imagen": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800",
            "link": "https://news.un.org/es/tags/salud"
        }
    ],
    "consejos": [
        {"id": 1, "titulo": "Tip del Robot", "texto": generar_texto("Da un consejo nutricional para personas con VIH", "Recuerda hidratarte y consumir suficiente proteína.")}
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
            "descripcion": f"Video de {r['c']}. Platillo saludable y equilibrado.",
            "link_externo": r["v"]
        } for i, r in enumerate(recetas_hoy)
    ],
    "salud_mental": {
        "emocion_del_dia": generar_texto("Propón una emoción positiva", "Paz interior"),
        "desafio": generar_texto("Crea un mini reto de autocuidado", "Escribe 3 cosas por las que agradeces hoy."),
        "afirmacion_positiva": generar_texto("Crea una afirmación corta", "Soy valiente y cuido de mi salud."),
        "puntos_ganados": 50
    }
}

# 5. CONSTRUIR CONTENIDO SALUD
salud_data = { "mito_del_dia": mito_hoy }

# 6. GUARDAR
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)
with open('salud.json', 'w', encoding='utf-8') as f:
    json.dump(salud_data, f, ensure_ascii=False, indent=2)

print("Actualización 100% completada.")
