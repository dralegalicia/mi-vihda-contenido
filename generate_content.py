import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# 1. Configuración de API
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: La variable GEMINI_API_KEY no existe en los Secrets de GitHub.")
    exit(1)

genai.configure(api_key=api_key)

# 2. Configuración del Modelo (Nombre exacto)
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt, fallback):
    try:
        # Prompt más estricto para evitar textos largos o basura
        full_prompt = f"{prompt}. Responde directamente en español, sin introducciones, máximo 200 caracteres."
        response = model.generate_content(full_prompt)
        if response and response.text:
            return response.text.strip()
        return fallback
    except Exception as e:
        print(f"Error llamando a Gemini: {e}")
        return fallback

# 3. Listas de respaldo (Fallback)
RECETAS = [
    {"nombre": "Ensalada de Quinoa", "link": "https://www.youtube.com/watch?v=EdhZ2MD-dnE"},
    {"nombre": "Tacos de Pescado", "link": "https://www.youtube.com/watch?v=7taoXVgZ24Q"}
]

# 4. Generación de datos
receta_hoy = random.choice(RECETAS)

data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu asistente inteligente está listo para acompañarte hoy.",
        "activo": True
    },
    "noticias": [{
        "id": 1,
        "titulo": "Avances en Salud 2024",
        "resumen": generar_texto("Resume una noticia de salud positiva breve.", "Mantener una buena alimentación fortalece tu sistema inmune cada día."),
        "url_imagen": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800",
        "link": "https://news.un.org/es/tags/salud"
    }],
    "consejos": [{
        "id": 1,
        "titulo": "Consejo del Día",
        "texto": generar_texto("Da un consejo breve de nutrición para VIH.", "Recuerda incluir siempre vegetales verdes en tus comidas.")
    }],
    "recetas": [{
        "id": 1,
        "nombre": receta_hoy["nombre"],
        "url_imagen": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
        "descripcion": generar_texto(f"Beneficios de {receta_hoy['nombre']}", "Platillo equilibrado rico en nutrientes esenciales."),
        "link_externo": receta_hoy["link"]
    }],
    "salud_mental": {
        "emocion_del_dia": "Motivación",
        "desafio": generar_texto("Un desafío de autocuidado.", "Dedica 5 minutos a respirar profundamente."),
        "afirmacion_positiva": "Mi salud es mi mayor tesoro.",
        "puntos_ganados": 50
    }
}

# 5. Guardar JSON
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("¡Archivo JSON generado con éxito!")
