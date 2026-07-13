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

# 2. NUEVA BIBLIOTECA DE RECETAS CON IMÁGENES Y ENLACES WEB / PLATAFORMAS
# Se eliminó la dependencia directa del reproductor de YouTube.
BIBLIOTECA_RECETAS = [
    {
        "n": "Tacos de Lechuga con Cochinita Pibil", 
        "img": "https://unsplash.com", 
        "link": "https://www.kiwilimon.com/receta/recetas-de-botanas-faciles/botanitas-mexicanas/tacos-de-lechuga-con-cochinita-pibil",
        "fuente": "Kiwilimón"
    },
    {
        "n": "Sopa de Lentejas Tradicional", 
        "img": "https://unsplash.com", 
        "link": "https://www.mexicoenmicocina.com/receta-sopa-de-lentejas/",
        "fuente": "México en mi Cocina"
    },
    {
        "n": "Pescado al Horno con Verduras", 
        "img": "https://unsplash.com", 
        "link": "https://cheforopeza.com.mx",
        "fuente": "Chef Oropeza"
    },
    {
        "n": "Ensalada de Quinoa con Verduras", 
        "img": "https://unsplash.com", 
        "link": "https://kiwilimon.com",
        "fuente": "Kiwilimón"
    },
    {
        "n": "Caldo de Pollo con Verduras", 
        "img": "https://unsplash.com", 
        "link": "https://jaujacinamexicana.com",
        "fuente": "Jauja Cocina"
    },
    {
        "n": "Ceviche de Pescado Tradicional", 
        "img": "https://unsplash.com", 
        "link": "https://cheforopeza.com.mx",
        "fuente": "Chef Oropeza"
    }
]

# Seleccionamos 2 recetas al azar de la biblioteca para el contenido diario
recetas_hoy = random.sample(BIBLIOTECA_RECETAS, 2)

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
            "url_imagen": r["img"],
            "descripcion": f"Prepara un delicioso platillo de la mano de {r['fuente']}. Haz clic para ver los ingredientes y pasos completos en su sitio oficial.",
            "link_externo": r["link"]
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

print("¡Contenido generado exitosamente sin dependencias de video!")
