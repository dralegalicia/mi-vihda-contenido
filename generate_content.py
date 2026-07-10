import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# 1. Configuración de API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Listas de contenido sincronizado
RECETAS = [
    {"nombre": "Ensalada de Quinoa", "link": "https://www.youtube.com/watch?v=EdhZ2MD-dnE"},
    {"nombre": "Tacos de Pescado con Aguacate", "link": "https://www.youtube.com/watch?v=7taoXVgZ24Q"},
    {"nombre": "Batido Energético Natural", "link": "https://www.youtube.com/watch?v=DMw2uZ9A2fc"}
]

OBESIDAD = [
    {"titulo": "Manejo del Peso y VIH", "link": "https://www.youtube.com/watch?v=ZMv3FjYCKbE"},
    {"titulo": "Entendiendo la Obesidad", "link": "https://www.youtube.com/watch?v=CndXAtXPfhw"}
]

# 3. Usar el modelo correcto y actual
# Usamos gemini-1.5-flash directamente, es el estándar actual
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error al generar: {str(e)}"

# 4. Generación dinámica
receta_hoy = random.choice(RECETAS)
obesidad_hoy = random.choice(OBESIDAD)

data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "recursos_obesidad": [{
        "id": 1,
        "titulo": obesidad_hoy["titulo"],
        "descripcion": generar_texto(f"Escribe una descripción empática y breve sobre '{obesidad_hoy['titulo']}' para pacientes con VIH."),
        "link": obesidad_hoy["link"]
    }],
    "noticias": [{
        "id": 1,
        "titulo": "Actualidad en Salud Global",
        "resumen": generar_texto("Resume una noticia esperanzadora sobre avances en salud para personas con VIH."),
        "url_imagen": "https://images.unsplash.com/photo-1532938890184-2a6c8e318991?auto=format&fit=crop&w=800",
        "link": "https://news.un.org/es/tags/salud"
    }],
    "consejos": [{
        "id": 1,
        "titulo": "Consejo de Bienestar Diario",
        "texto": generar_texto("Escribe un consejo de nutrición profesional y cariñoso para alguien que vive con VIH.")
    }],
    "recetas": [{
        "id": 1,
        "nombre": receta_hoy["nombre"],
        "url_imagen": f"https://source.unsplash.com/featured/?{receta_hoy['nombre'].replace(' ', ',')}",
        "descripcion": generar_texto(f"Describe los beneficios nutricionales de: {receta_hoy['nombre']}."),
        "link_externo": receta_hoy["link"]
    }],
    "salud_mental": {
        "emocion_del_dia": "Equilibrio",
        "desafio": generar_texto("Propón un pequeño desafío de salud mental para hoy."),
        "afirmacion_positiva": generar_texto("Escribe una afirmación de poder para alguien viviendo con VIH."),
        "puntos_ganados": 50
    }
}

# 5. Guardar JSON
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("¡Proceso terminado con éxito!")
