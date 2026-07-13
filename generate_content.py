import os
import json
import random
import google.generativeai as genai

# Configuración de la API con validación básica
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: La variable GEMINI_API_KEY no está configurada.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_info_ia(prompt, fallback):
    """Genera texto profesional y médico con manejo de errores."""
    try:
        response = model.generate_content(
            f"{prompt}. Responde en español, máximo 250 caracteres, tono empático, profesional y basado en evidencia médica."
        )
        # Limpiamos caracteres que podrían romper el JSON
        return response.text.strip().replace('"', "'") if response.text else fallback
    except Exception as e:
        print(f"Error generando contenido: {e}")
        return fallback

def generar_url_imagen(tema):
    """Genera una URL de imagen dinámica garantizando que siempre sea una petición nueva."""
    # Usamos un número aleatorio para evitar que Android/App cachee la imagen vieja
    return f"https://source.unsplash.com/800x600/?{tema},medical&{random.randint(1000, 9999)}"

# --- BIBLIOTECA DE VIDEOS VERIFICADOS ---
VIDEOS_VERIFICADOS = [
    {"n": "Batido Verde Saludable", "v": "https://www.youtube.com/embed/9w_0UqN0YQ4", "c": "Canal Salud"},
    {"n": "Pescado al Horno con Verduras", "v": "https://www.youtube.com/embed/9vN5Y4k95-E", "c": "Cocina Sana"},
    {"n": "Ensalada Completa", "v": "https://www.youtube.com/embed/8JgS6a7D_48", "c": "Nutrición Hoy"}
]

# --- PROCESO DE GENERACIÓN ---
recetas_hoy = random.sample(VIDEOS_VERIFICADOS, 2)

data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu bienestar es nuestra meta. Consulta a tu médico regularmente.",
        "url_imagen": generar_url_imagen("nature")
    },
    "salud": {
        "mito": obtener_info_ia("Dame un mito común sobre el VIH", "Mito: El VIH se transmite por contacto casual."),
        "realidad": obtener_info_ia("Dame la realidad científica que desmiente el mito de que el VIH se transmite por contacto casual", "Realidad: El VIH no se transmite por abrazos, besos, compartir baños o utensilios."),
        "url_imagen": generar_url_imagen("science")
    },
    "noticias": {
        "titulo": "Actualidad en Salud",
        "resumen": obtener_info_ia("Resume un avance reciente en el tratamiento del VIH para pacientes", "Los tratamientos actuales permiten una excelente calidad de vida y salud a largo plazo."),
        "link": "https://clinicalinfo.hiv.gov/es",
        "url_imagen": generar_url_imagen("hospital")
    },
    "consejos": {
        "titulo": "Consejo del día",
        "texto": obtener_info_ia("Da un consejo nutricional para fortalecer el sistema inmune en pacientes con VIH", "Consume alimentos frescos, ricos en antioxidantes y mantente siempre hidratado."),
        "url_imagen": generar_url_imagen("food")
    },
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": generar_url_imagen("cooking"),
            "descripcion": f"Receta recomendada por {r['c']}.",
            "link_externo": r["v"]
        } for i, r in enumerate(recetas_hoy)
    ]
}

# --- GUARDADO ---
try:
    with open('data_app.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Archivo 'data_app.json' generado correctamente.")
except Exception as e:
    print(f"Error al guardar el archivo: {e}")
