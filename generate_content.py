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
        response = model.generate_content(prompt + ". Responde directamente en español, máximo 200 caracteres.")
        return response.text.strip() if response.text else fallback
    except:
        return fallback

# 2. Biblioteca de Videos Reales (Canales de Cocina Saludable)
RECETAS_MASTER = [
    {"n": "Tacos de Lechuga Saludables", "v": "https://www.youtube.com/watch?v=kYI_t9M3q6s", "c": "Kiwilimón"},
    {"n": "Sopa de Verduras y Lentejas", "v": "https://www.youtube.com/watch?v=7M5_V0I9m68", "c": "Kiwilimón"},
    {"n": "Pescado a la Veracruzana", "v": "https://www.youtube.com/watch?v=F_YF-9H0b90", "c": "Chef Oropeza"},
    {"n": "Guiso de Lentejas Casero", "v": "https://www.youtube.com/watch?v=84u0C-m9O80", "c": "Cocina con Addy"}
]
recetas_hoy = random.sample(RECETAS_MASTER, 2)

# 3. Construcción del JSON que la App espera
data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu bienestar es nuestra prioridad. Usa la calculadora para consejos personalizados.",
        "activo": True
    },
    "noticias": [
        {
            "id": 1,
            "titulo": "Avances en Salud Preventiva",
            "resumen": generar_texto("Resume una noticia breve de salud positiva", "La prevención es la base de una vida plena y saludable."),
            "url_imagen": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800",
            "link": "https://news.un.org/es/tags/salud"
        }
    ],
    "consejos": [
        {"id": 1, "titulo": "Tip del Día", "texto": generar_texto("Da un consejo de nutrición para VIH", "Consume suficientes proteínas para fortalecer tus músculos.")}
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
            "descripcion": f"Video saludable de {r['c']}.",
            "link_externo": r["v"] # Enviamos el link completo para que funcione el clic
        } for i, r in enumerate(recetas_hoy)
    ],
    "salud_mental": {
        "emocion_del_dia": generar_texto("Dime una emoción positiva", "Gratitud"),
        "desafio": generar_texto("Crea un mini reto de psicología positiva", "Escribe tres cosas buenas que te pasaron hoy."),
        "afirmacion_positiva": generar_texto("Crea una afirmación de poder", "Soy fuerte y tengo el control de mi salud."),
        "puntos_ganados": 50
    }
}

# 4. Guardar como contenido_nutri.json (Nombre exacto que busca la App)
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("¡Archivos generados correctamente!")
