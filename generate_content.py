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

# 2. BIBLIOTECA DE RECETAS WEB Y TIKTOK (Mucho más estables que YouTube)
RECURSOS_HOY = [
    {"n": "Recetario para Diabéticos", "u": "https://www.cocinafacil.com.mx/recetas-para-diabeticos/", "f": "Cocina Fácil", "img": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800"},
    {"n": "Ensalada de Quinoa (Paso a paso)", "u": "https://www.kiwilimon.com/receta/ensaladas/ensalada-de-quinoa-con-verduras", "f": "Kiwilimón", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"},
    {"n": "Consejos del Chef Oropeza", "u": "https://www.tiktok.com/@cheforopeza", "f": "TikTok Oficial", "img": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800"},
    {"n": "Cocina Saludable en TikTok", "u": "https://www.tiktok.com/discover/cocina-saludable-mexico", "f": "TikTok Salud", "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"},
    {"n": "Guía de Alimentación OPS/OMS", "u": "https://www.paho.org/es/temas/alimentacion-sana", "f": "Organización Mundial de la Salud", "img": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800"}
]

# Seleccionamos 2 recursos al azar
seleccion = random.sample(RECURSOS_HOY, 2)

# 3. Construcción del JSON
data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Hoy el robot ha seleccionado recursos de TikTok y guías web para tu salud.",
        "activo": True
    },
    "noticias":
