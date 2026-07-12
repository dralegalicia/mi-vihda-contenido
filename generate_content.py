import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# 1. Configuración de API con validación estricta
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Esto es vital: si esto falla, sabremos exactamente qué pasa
    print("ERROR CRÍTICO: La variable GEMINI_API_KEY no está definida en el entorno.")
    exit(1)

genai.configure(api_key=api_key)

# 2. Listas de contenido
RECETAS = [
    {"nombre": "Ensalada de Quinoa", "link": "https://www.youtube.com/watch?v=EdhZ2MD-dnE"},
    {"nombre": "Tacos de Pescado con Aguacate", "link": "https://www.youtube.com/watch?v=7taoXVgZ24Q"},
    {"nombre": "Batido Energético Natural", "link": "https://www.youtube.com/watch?v=DMw2uZ9A2fc"}
]

OBESIDAD = [
    {"titulo": "Manejo del Peso y VIH", "link": "https://www.youtube.com/watch?v=ZMv3FjYCKbE"},
    {"titulo": "Entendiendo la Obesidad", "link": "https://www.youtube.com/watch?v=CndXAtXPfhw"}
]

model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt):
    try:
        # Se añade un pequeño delay o manejo de errores de red si es necesario
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error en generación: {str(e)}"

# 3. Generación
receta_hoy = random.choice(RECETAS)
obesidad_hoy = random.choice(OBESIDAD)

data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "recursos_obesidad": [{
        "id": 1,
        "titulo": obesidad_hoy["titulo"],
        "descripcion": generar_texto(f"Descripción breve y empática para pacientes con VIH sobre: {obesidad_hoy['titulo']}"),
        "link": obesidad_hoy["link"]
    }],
    "noticias": [{
        "id": 1,
        "titulo": "Actualidad en Salud Global",
        "resumen": generar_texto("Resume una noticia positiva sobre VIH."),
        "url_imagen": "https://images.unsplash.com/photo-1532938890184-2a6c8e318991?auto=format&fit=crop&w=800",
        "link": "https://news.un.org/es/tags/salud"
    }],
    "consejos": [{
        "id": 1,
        "titulo": "Consejo de Bienestar Diario",
        "texto": generar_texto("Consejo nutricional profesional y cariñoso para alguien con VIH.")
    }],
    "recetas": [{
        "id": 1,
        "nombre": receta_hoy["nombre"],
        "url_imagen": f"https://source.unsplash.com/featured/?{receta_hoy['nombre'].replace(' ', ',')}",
        "descripcion": generar_texto(f"Beneficios nutricionales de: {receta_hoy['nombre']}"),
        "link_externo": receta_hoy["link"]
    }],
    "salud_mental": {
        "emocion_del_dia": "Equilibrio",
        "desafio": generar_texto("Un pequeño desafío de salud mental para hoy."),
        "afirmacion_positiva": generar_texto("Afirmación de poder para alguien viviendo con VIH."),
        "puntos_ganados": 50
    }
}

# 4. Guardar JSON
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("¡Proceso terminado con éxito!")
