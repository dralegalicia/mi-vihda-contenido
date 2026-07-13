import os
import json
import random
import google.generativeai as genai

# Configuración
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto(prompt, fallback):
    """Genera texto con un fallback seguro"""
    try:
        response = model.generate_content(prompt + ". Responde en español, máximo 200 caracteres.")
        return response.text.strip().replace('"', "'") if response.text else fallback
    except:
        return fallback

# --- BIBLIOTECA VERIFICADA DE VIDEOS ---
# Asegúrate de que estos links abran directamente en un navegador o reproductor
RECETAS_MASTER = [
    {"n": "Tacos de Lechuga con Pollo", "v": "https://www.youtube.com/embed/kYI_t9M3q6s", "c": "Kiwilimón"},
    {"n": "Sopa de Verduras", "v": "https://www.youtube.com/embed/7M5_V0I9m68", "c": "Kiwilimón"},
    {"n": "Pescado a la Veracruzana", "v": "https://www.youtube.com/embed/F_YF-9H0b90", "c": "Chef Oropeza"}
]

# --- CONTENIDO ---
recetas_hoy = random.sample(RECETAS_MASTER, 2)

nutri_data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu salud es nuestra prioridad. Sigue estas recomendaciones diarias.",
        "activo": True
    },
    "noticias": [
        {
            "titulo": generar_texto("Dame un título corto sobre un avance médico reciente en VIH", "Avances en Tratamiento"),
            "resumen": generar_texto("Resume una noticia real de salud pública", "La prevención y el control médico son esenciales para una vida plena."),
            "link": "https://www.google.com/search?q=noticias+salud+VIH+mexico"
        }
    ],
    "consejos": [
        {
            "titulo": "Consejo del día", 
            "texto": generar_texto("Da un consejo nutricional muy breve para personas con VIH", "Mantén una dieta equilibrada y rica en nutrientes.")
        }
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400",
            "descripcion": f"Receta saludable por {r['c']}",
            "link_externo": r["v"] 
        } for i, r in enumerate(recetas_hoy)
    ]
}

# Guardar
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)

print("Actualización lista.")
