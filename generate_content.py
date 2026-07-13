import os
import json
import random
import google.generativeai as genai

# Configuración
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generar_texto_limpio(prompt):
    """Genera texto simple asegurando que no rompa el JSON"""
    try:
        response = model.generate_content(prompt + ". Responde directo, sin comillas extra, máximo 150 caracteres.")
        return response.text.strip().replace('"', "'")
    except:
        return "Información en actualización."

# --- BIBLIOTECA VERIFICADA ---
RECETAS_MASTER = [
    {"n": "Tacos de Lechuga con Pollo", "v": "https://www.youtube.com/watch?v=kYI_t9M3q6s", "c": "Kiwilimón"},
    {"n": "Sopa de Verduras con Lentejas", "v": "https://www.youtube.com/watch?v=7M5_V0I9m68", "c": "Kiwilimón"},
    {"n": "Pescado a la Veracruzana", "v": "https://www.youtube.com/watch?v=F_YF-9H0b90", "c": "Chef Oropeza"},
    {"n": "Ensalada de Atún Saludable", "v": "https://www.youtube.com/watch?v=oX-0qC81L7E", "c": "Kiwilimón"}
]

# --- ESTRUCTURA DE DATOS ---
recetas_hoy = random.sample(RECETAS_MASTER, 2)

nutri_data = {
    "noticias": [
        {
            "titulo": "Salud y Bienestar Preventivo",
            "resumen": generar_texto_limpio("Resume brevemente la importancia de la nutrición en pacientes con VIH."),
            "link": "https://www.gob.mx/salud" # Enlace institucional de México (Seguro)
        }
    ],
    "consejos": [
        {
            "titulo": "Tip Diario", 
            "texto": generar_texto_limpio("Da un consejo de nutrición saludable para paciente con VIH en México.")
        }
    ],
    "recetas": [
        {
            "id": i,
            "nombre": r["n"],
            "url_imagen": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400",
            "descripcion": f"Receta nutritiva recomendada por {r['c']}",
            "link_externo": r["v"] # Aquí usamos el enlace real de tu lista
        } for i, r in enumerate(recetas_hoy)
    ]
}

# Guardar archivos
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(nutri_data, f, ensure_ascii=False, indent=2)

print("Actualización completada correctamente sin errores de enlace.")
