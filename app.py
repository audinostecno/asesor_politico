import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Asesor Político IA", page_icon="🇦🇷", layout="centered")
st.title("🏛️ Asesor Político y Técnico - Edición La Pampa")
st.markdown("Asistente conectado a datos oficiales (OpenArg) y documentos provinciales.")

# 2. Cargar las claves de seguridad de forma segura (desde los secretos de Streamlit)
# En local, esto se lee de un archivo .streamlit/secrets.toml
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
OPENARG_MCP_KEY = st.secrets["OPENARG_API_KEY"]

# Configurar Gemini
genai.configure(api_key=GOOGLE_API_KEY)
modelo = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido y potente

# 3. Inicializar el historial de chat en la memoria de la página
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar el historial de mensajes
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# 4. Caja de texto para que el usuario pregunte
prompt = st.chat_input("Ej: ¿Cuál es el presupuesto nacional de educación o la inflación según INDEC?")

if prompt:
    # Mostrar el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})

    # 5. Aquí va la conexión con la IA (y próximamente el MCP de OpenArg)
    with st.chat_message("assistant"):
        # NOTA: Aquí estructuraremos el código para que primero consulte a OpenArg si requiere datos duros.
        # Por ahora, hacemos la consulta directa a Gemini.
        respuesta = modelo.generate_content(prompt)
        st.markdown(respuesta.text)
        
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta.text})