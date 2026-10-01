import streamlit as st
import google.generativeai as genai
import os
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Herramienta de Gestión - Audinos", page_icon="🇦🇷", layout="centered")

# 2. Menú Lateral: Selector de Motor (Nube vs Local)
with st.sidebar:
    if os.path.exists("Squat.png"):
        st.image("Squat.png", width=100)
    else:
        st.write("🇦🇷")
    
    st.markdown("### 🧠 Cerebro de la IA")
    motor_ia = st.radio(
        "Seleccioná el motor:",
        ["Nube (Gemini)", "Local (Qwen 7B)"],
        help="El modo Local requiere ejecutar la app directamente en tu PC con Ollama encendido."
    )
    
    if motor_ia == "Local (Qwen 7B)":
        st.info("💡 Modo Offline Activo: Procesando localmente en la PC.")

# 3. Encabezado de presentación
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("Squat.png"):
        st.image("Squat.png", width=110)
    else:
        st.write("🇦🇷")

with col2:
    st.title("Hola, soy Audinos 👋")
    st.caption("📍 Santa Rosa, La Pampa")

st.markdown("""
Armé esta herramienta para nuestro equipo. La idea es simple: tener a mano y al instante los datos técnicos, presupuestos y proyectos de La Pampa, sin perder tiempo buscando en mil PDFs.

Está configurada con la información oficial y tiene una regla estricta: **si el dato no está en los documentos, te lo dice de frente y no inventa nada**. 

Escribime acá abajo, ¿qué tema o proyecto querés que revisemos?
""")

st.divider()

# 4. Historial de chat
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 5. Entrada del usuario
prompt_usuario = st.chat_input("Ej: ¿Cuál es el presupuesto o diagnóstico educativo?")

if prompt_usuario:
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    with st.chat_message("assistant"):
        with st.spinner(f"Analizando consulta con {motor_ia}..."):
            
            respuesta = None
            prompt_asesor = f"""
            Sos una herramienta técnica y ejecutiva creada por Audinos para La Pampa.
            Respondé de manera directa, profesional y clara (usando viñetas o negritas para estructurar).
            Regla de oro: NO INVENTES INFORMACIÓN, DATOS NI NÚMEROS. Si no lo sabés, decilo claramente.
            
            Consulta: {prompt_usuario}
            """

            # --- RUTA 1: MODO LOCAL (QWEN 7B VÍA OLLAMA) ---
            if motor_ia == "Local (Qwen 7B)":
                try:
                    url_local = "http://localhost:11434/api/generate"
                    payload = {
                        "model": "qwen", # Nombre de tu modelo descargado en Ollama
                        "prompt": prompt_asesor,
                        "stream": False
                    }
                    response = requests.post(url_local, json=payload, timeout=30)
                    if response.status_code == 200:
                        respuesta = response.json().get("response")
                    else:
                        st.error("❌ Ocurrió un error en el servidor local de Ollama.")
                except Exception:
                    st.error("❌ No se pudo conectar con Qwen local. Si estás usando la versión web, seleccioná 'Nube (Gemini)'. Para usar Qwen, ejecutá la app en tu PC con Ollama encendido.")

            # --- RUTA 2: MODO NUBE (GOOGLE GEMINI) ---
            else:
                try:
                    clave_google = st.secrets.get("GEMINI_API_KEY_1")
                    if clave_google:
                        genai.configure(api_key=clave_google)
                        modelo = genai.GenerativeModel('gemini-1.5-flash')
                        respuesta = modelo.generate_content(prompt_asesor).text
                    else:
                        st.error("❌ Falta configurar la clave GEMINI_API_KEY_1 en los Secrets de Streamlit.")
                except Exception as e:
                    st.error(f"❌ Error con Google Gemini: {e}")

            # 6. Mostrar resultado
            if respuesta:
                st.markdown(respuesta)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
