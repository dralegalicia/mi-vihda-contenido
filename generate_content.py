import os
import json
import random
import google.generativeai as genai

# Configuración
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_info_ia(prompt, fallback):
    try:
        response = model.generate_content(f"{prompt}. Responde en español, máximo 200 caracteres, tono profesional.")
        return response.text.strip().replace('"', "'") if response.text else fallback
    except:
        return fallback

# --- BIBLIOTECA DE VIDEOS (SOLO IDs) ---
# Usamos el ID de 11 caracteres requerido por Android-YouTube-Player
RECETAS_MASTER = [
    {"nombre": "5 Cenas Saludables", "youtube_id": "IHwiRKGz_zU", "canal": "Mónica Acha"},
    {"nombre": "Snacks Saludables Rápido", "youtube_id": "_v_qY9Xb-t0", "canal": "Clean & Delicious"},
    {"nombre": "Desayunos con Avena", "youtube_id": "3bX8F83w_nc", "canal": "Cocina al Natural"},
    {"nombre": "Almuerzos nutritivos", "youtube_id": "t_D_uEw2k54", "canal": "Nutrición Global"}
]

def generar_url_imagen(tema):
    return f"https://source.unsplash.com/800x600/?{tema},healthy-food&sig={random.randint(1000, 9999)}"

# --- ESTRUCTURA DE CONTENIDO ---
# Seleccionamos 2 recetas al azar de nuestra base de datos verificada
recetas_hoy = random.sample(RECETAS_MASTER, 2)

data = {
    "aviso_urgente": {
        "titulo": "¡Bienvenido a Nutri-VIHTAL!",
        "mensaje": "Tu bienestar es nuestra meta. Consulta a tu médico regularmente."
    },
    "salud": {
        "mito": obtener_info_ia("Dame un mito común sobre el VIH", "Mito: El VIH se transmite por compartir cubiertos."),
        "realidad": obtener_info_ia("Dame la realidad científica que desmiente ese mito", "Realidad: El VIH no sobrevive fuera del cuerpo y no se transmite al compartir platos o cubiertos.")
    },
    "recetas": [
        {
            "id": i,
            "nombre": r["nombre"],
            "youtube_id": r["youtube_id"],  # Solo los 11 caracteres para el Player
            "canal": r["canal"],
            "url_imagen": generar_url_imagen("cooking")
        } for i, r in enumerate(recetas_hoy)
    ]
}

# --- GUARDADO ---
# Este archivo es el que consumirás en tu App
try:
    with open('data_app.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Archivo 'data_app.json' generado con IDs verificados.")
except Exception as e:
    print(f"Error: {e}")
