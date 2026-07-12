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
        full_prompt = f"{prompt}. Responde directamente en español, máximo 200 caracteres."
        response = model.generate_content(full_prompt)
        return response.text.strip() if response.text else fallback
    except:
        return fallback

def generar_mito_trivia():
    temas = ["VIH", "Riesgo Cardiovascular", "Salud Mental", "PrEP", "DoxiPrEP", "Hipertensión", "Diabetes"]
    tema = random.choice(temas)
    
    prompt = f"""
    Genera un mito de salud sobre {tema} para una aplicación.
    Responde ÚNICAMENTE con el objeto JSON puro, sin ```json ni nada extra.
    {{
      "tema": "{tema}",
      "mito": "escribe un mito corto",
      "realidad": "escribe la realidad breve",
      "pregunta": "haz una pregunta de trivia",
      "opciones": ["opcion1", "opcion2", "opcion3"],
      "respuesta_correcta": 0,
      "explicacion_ia": "mensaje de aliento del robot"
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Limpiador de seguridad para el JSON
        texto = response.text.strip()
        if "{" in texto:
            texto = texto[texto.find("{"):texto.rfind("}")+1]
        return json.loads(texto)
    except Exception as e:
        print(f"Error en mito: {e}")
        return None

# 2. Base de datos de Recetas y Videos (Corregidos)
BIBLIOTECA_RECETAS = [
    {
        "nombre": "Ensalada de Quinoa con Pollo",
        "video": "https://www.youtube.com/watch?v=SAn8v-qS1Zk",
        "imagen": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800"
    },
    {
        "nombre": "Sopa de Lentejas Casera",
        "video": "https://www.youtube.com/watch?v=mZ-vM76rGnk",
        "imagen": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"
    },
    {
        "nombre": "Tacos de Pescado Saludables",
        "video": "https://www.youtube.com/watch?v=84u0C-m9O80",
        "imagen": "https://images.unsplash.com/photo-1512132411229-c30391241dd8?w=800"
    }
]

# 3. Generación integrada
receta_hoy = random.choice(BIBLIOTECA_RECETAS)
mito_hoy = generar_mito_trivia()

data = {
    "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "aviso_urgente": {
        "titulo": "¡Nuevo Contenido!",
        "mensaje": "El robot ha actualizado tus noticias y el reto del día.",
        "activo": True
    },
    "mito_del_dia": mito_hoy,
    "noticias": [{
        "id": 1,
        "titulo": "Bienestar Integral 2024",
        "resumen": generar_texto("Resume una noticia positiva de salud breve", "Cuidar tu cuerpo es la mejor inversión para tu futuro."),
        "url_imagen": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800",
        "link": "https://news.un.org/es/tags/salud"
    }],
    "consejos": [{"id": 1, "titulo": "Sabías que...", "texto": generar_texto("Da un consejo breve de nutrición para VIH", "La hidratación mejora la absorción de tus medicamentos.")}],
    "recetas": [{
        "id": 1,
        "nombre": receta_hoy["nombre"],
        "url_imagen": receta_hoy["imagen"],
        "descripcion": f"Aprende a preparar {receta_hoy['nombre']}, un platillo equilibrado y delicioso.",
        "link_externo": receta_hoy["video"]
    }],
    "salud_mental": {
        "emocion_del_dia": "Motivación",
        "desafio": "Haz 10 minutos de estiramientos ligeros.",
        "afirmacion_positiva": "Mi salud está en mis manos y hoy decido cuidarla.",
        "puntos_ganados": 50
    }
}

# 4. Guardar archivo
with open('contenido_nutri.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("¡Contenido actualizado correctamente!")
