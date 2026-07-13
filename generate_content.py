import os
import json
import random
import google.generativeai as genai

# Configuración
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_info_ia(prompt, fallback):
    """Genera contenido médico basado en fuentes confiables"""
    try:
        contexto = "Actúa como un médico experto. Usa información de fuentes como NIH (clinicalinfo.hiv.gov) y la OPS."
        response = model.generate_content(f"{contexto} {prompt}. Máximo 200 caracteres, tono profesional y esperanzador.")
        return response.text.strip().replace('"', "'") if response.text else fallback
    except:
        return fallback

def generar_url_imagen(tema):
    """Genera una URL de imagen dinámica y profesional"""
    # Usamos temas específicos para asegurar que la imagen sea adecuada para salud
    # Los parámetros de Unsplash garantizan alta calidad
    return f"https://source.unsplash.com/featured/?{tema},medical,wellness,healthy-food&sig={random.randint(1, 1000)}"

# --- BIBLIOTECA DE VIDEOS ---
RECETAS_MASTER = [
    {"n": "Tacos de Lechuga con Pollo", "v": "https://www.youtube.com/embed/kYI_t9M3q6s", "c": "Kiwilimón"},
    {"n": "Sopa de Verduras", "v": "https://www.youtube.com/embed/7M5_V0I9m68", "c": "Kiwilimón"},
    {"n": "Pescado a la Veracruzana", "v": "https://www.youtube.com/embed/F_YF-9H0b90", "c": "Chef Oropeza"}
]

# --- ESTRUCTURA DE DATOS ---
recetas_hoy = random.sample(RECETAS_MASTER, 2)

nutri_data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu bienestar es nuestra meta. Consulta siempre a tu médico.",
        "activo": True,
        "url_imagen": generar_url_imagen("nature,peaceful")
    },
    "noticias": [
        {
            "titulo": "Actualidad Científica en VIH",
            "resumen": obtener_info_ia("Resumen breve sobre un avance reciente en el tratamiento del VIH.", 
                                      "La ciencia avanza diariamente en terapias que mejoran significativamente la calidad de vida."),
            "link": "https://clinicalinfo.hiv.gov/es",
            "url_imagen": generar_url_imagen("science,laboratory")
        }
    ],
    "consejos": [
        {
            "titulo": "Nutrición y Salud", 
            "texto": obtener_info_ia("Consejo nutricional para fortalecer el sistema inmune.", 
                                   "Una alimentación equilibrada es el mejor aliado de tu cuerpo."),
            "url_imagen": generar_url_imagen("fresh-vegetables,healthy-meal")
        }
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": generar_url_imagen("cooking,gourmet"),
            "descripcion": f"Receta recomendada por {r['c']}.",
            "link_externo": r["v"] 
        } for i, r in enumerate(recetas_hoy)
    ]
}

# Guardar archivos
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)

print("Actualización completada: Contenido y recursos visuales listos.")
