import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# Configuración
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Base de datos local: Parejas de título y link (para evitar desincronización)
RECETAS = [
    {"nombre": "Ensalada de Quinoa", "link": "https://www.youtube.com/watch?v=EdhZ2MD-dnE"},
    {"nombre": "Tacos de Pescado con Aguacate", "link": "https://www.youtube.com/watch?v=7taoXVgZ24Q"},
    {"nombre": "Batido Energético Natural", "link": "https://www.youtube.com/watch?v=DMw2uZ9A2fc"}
]

OBESIDAD = [
    {"titulo": "Manejo del Peso y VIH", "link": "https://www.youtube.com/watch?v=ZMv3FjYCKbE"},
    {"titulo": "Entendiendo la Obesidad", "link": "https://www.youtube.com/watch?v=CndXAtXPfhw"}
]

def generar_texto(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

# Selección aleatoria para el día de hoy
receta_hoy = random.choice(RECETAS)
obesidad_hoy = random.choice(OBESIDAD)

# Construcción del JSON
data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d"),
    "recursos_obesidad": [{
        "id": 1,
        "titulo": obesidad_hoy["titulo"],
        "descripcion": generar_texto(f"Escribe una descripción empática y breve sobre el tema '{obesidad_hoy['titulo']}' para pacientes con VIH."),
        "link": obesidad_hoy["link"]
    }],
    "noticias": [{
        "id": 1,
        "titulo": "Avances Globales en Salud",
        "resumen": generar_texto("Escribe un resumen breve y esperanzador sobre noticias actuales de salud y VIH."),
        "url_imagen": "https://images.unsplash.com/photo-1532938890184-2a6c8e318991?auto=format&fit=crop&w=800",
        "link": "https://news.un.org/es/tags/salud"
    }],
    "consejos": [{
        "id": 1,
        "titulo": "Consejo de Bienestar Diario",
        "texto": generar_texto("Escribe un consejo de autocuidado y nutrición, cálido y profesional, para alguien que vive con VIH.")
    }],
    "recetas": [{
        "id": 1,
        "nombre": receta_hoy["nombre"],
        "url_imagen": f"https://source.unsplash.com/featured/?{receta_hoy['nombre'].replace(' ', ',')}",
        "descripcion": generar_texto(f"Describe brevemente los beneficios nutricionales de la receta: {receta_hoy['nombre']}."),
        "link_externo": receta_hoy["link"]
    }],
    "salud_mental": {
        "emocion_del_dia": "Equilibrio",
        "desafio": generar_texto("Propón un pequeño desafío de salud mental para el día de hoy."),
        "afirmacion_positiva": generar_texto("Escribe una afirmación de poder para alguien viviendo con VIH."),
        "puntos_ganados": 50
    }
}

# Guardar el archivo
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("¡Contenido actualizado correctamente con parejas sincronizadas!")
