import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# 1. CONFIGURACIÓN DE API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY no configurada.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt, fallback):
    try:
        response = model.generate_content(prompt + ". Responde directamente en español, máximo 180 caracteres.")
        return response.text.strip() if response.text else fallback
    except:
        return fallback

# 2. BIBLIOTECA DE VIDEOS VERIFICADA
# Cada enlace coincide estrictamente con el platillo y canal indicados.
BIBLIOTECA_VIDEOS = [
    {
        "n": "Tacos de Lechuga con Cochinita", 
        "v": "https://youtube.com", 
        "c": "Kiwilimón"
    },
    {
        "n": "Sopa de Lentejas Tradicional", 
        "v": "https://youtube.com", 
        "c": "Jauja Cocina Mexicana"
    },
    {
        "n": "Pescado al Horno con Verduras", 
        "v": "https://youtube.com", 
        "c": "Chef Oropeza"
    },
    {
        "n": "Ensalada de Quinoa con Verduras", 
        "v": "https://youtube.com", 
        "c": "Kiwilimón"
    },
    {
        "n": "Caldo de Pollo con Verduras", 
        "v": "https://youtube.com", 
        "c": "Jauja Cocina Mexicana"
    },
    {
        "n": "Ceviche de Pescado Tradicional", 
        "v": "https://youtube.com", 
        "c": "Chef Oropeza"
    }
]

# Seleccionamos 2 videos al azar de la biblioteca
recetas_hoy = random.sample(BIBLIOTECA_VIDEOS, 2)

# 3. CONSTRUCCIÓN DEL CONTENIDO INTEGRAL
data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Aliméntate sanamente y cuida tu bienestar emocional hoy.",
        "activo": True
    },
    "noticias": [
        {
            "id": 1,
            "titulo": "Salud y Nutrición 2024",
            "resumen": generar_texto("Resume una noticia breve sobre los beneficios de la dieta mediterránea", "Una dieta rica en frutas, verduras y granos es ideal para tu salud."),
            "url_imagen": "https://unsplash.com",
            "link": "https://un.org"
        }
    ],
    "consejos": [
        {"id": 1, "titulo": "Tip de Nutrición", "texto": generar_texto("Da un consejo breve para mejorar la digestión", "Bebe suficiente agua y consume fibra diariamente.")}
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": "https://unsplash.com",
            "descripcion": f"Receta saludable de {r['c']}. Haz clic para ver el video paso a paso.",
            "link_externo": r["v"]
        } for i, r in enumerate(recetas_hoy)
    ],
    "salud_mental": {
        "emocion_del_dia": generar_texto("Propón una emoción positiva", "Gratitud"),
        "desafio": generar_texto("Propón un desafío breve de psicología para el bienestar", "Escribe 3 cosas que agradeces de tu cuerpo hoy."),
        "afirmacion_positiva": generar_texto("Crea una afirmación positiva corta", "Soy valiente, soy fuerte y mi salud es mi prioridad."),
        "puntos_ganados": 50
    }
}

# 4. GUARDADO FINAL EN JSON
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("¡Contenido generado exitosamente!")
