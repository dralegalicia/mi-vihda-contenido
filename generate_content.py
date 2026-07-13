import os
import json
import random
import google.generativeai as genai

# Configuración de tu API Key de Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_info_ia(prompt, fallback):
    """Genera texto profesional y médico."""
    try:
        response = model.generate_content(f"{prompt}. Responde en español, máximo 250 caracteres, tono empático y profesional.")
        return response.text.strip().replace('"', "'") if response.text else fallback
    except:
        return fallback

def generar_url_imagen(tema):
    """Genera una imagen aleatoria de alta calidad desde Unsplash."""
    return f"https://source.unsplash.com/featured/?{tema},medical,wellness&sig={random.randint(1, 1000)}"

# --- BIBLIOTECA DE VIDEOS VERIFICADOS ---
# Links en formato embed para que se reproduzcan dentro de tu app
VIDEOS_VERIFICADOS = [
    {"n": "Batido Verde Saludable", "v": "https://www.youtube.com/embed/9w_0UqN0YQ4", "c": "Canal Salud"},
    {"n": "Receta de Pescado al Horno", "v": "https://www.youtube.com/embed/9vN5Y4k95-E", "c": "Cocina Sana"},
    {"n": "Ensalada Completa", "v": "https://www.youtube.com/embed/8JgS6a7D_48", "c": "Nutrición Hoy"}
]

# --- ESTRUCTURA DE CONTENIDO ---
recetas_hoy = random.sample(VIDEOS_VERIFICADOS, 2)

# Este es el archivo final que tu app descargará cada día
data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu bienestar es nuestra meta. Consulta a tu médico regularmente.",
        "url_imagen": generar_url_imagen("nature")
    },
    "salud": {
        "mito": obtener_info_ia("Dame un mito común sobre el VIH", "Mito: El VIH se transmite por compartir utensilios."),
        "realidad": obtener_info_ia("Dame la realidad científica que desmiente ese mito sobre el VIH", "Realidad: El VIH no sobrevive fuera del cuerpo y no se transmite por compartir objetos."),
        "url_imagen": generar_url_imagen("science")
    },
    "noticias": {
        "titulo": "Avance Médico",
        "resumen": obtener_info_ia("Resume un avance reciente en el tratamiento del VIH", "Los tratamientos actuales son muy efectivos y permiten una excelente calidad de vida."),
        "link": "https://clinicalinfo.hiv.gov/es",
        "url_imagen": generar_url_imagen("hospital")
    },
    "consejos": {
        "titulo": "Consejo del día",
        "texto": obtener_info_ia("Da un consejo nutricional para fortalecer el sistema inmune en pacientes con VIH", "Consume alimentos ricos en antioxidantes y mantente hidratado."),
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

# Guardar todo en un archivo JSON único
with open('data_app.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Contenido actualizado exitosamente en data_app.json")
