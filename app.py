import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Asesor Político IA", page_icon="🏛️", layout="centered")
st.title("🏛️ Asesor Político y Técnico")
st.markdown("Hola soy Audinos. ¿En qué puedo ayudarte?")

# 2. Inicializar el historial de chat en la memoria de la página
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar el historial de mensajes al cargar la página
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 3. Caja de texto para que el usuario pregunte
prompt_usuario = st.chat_input("Escribí tu consulta política, presupuestaria o técnica...")

if prompt_usuario:
    # Mostrar el mensaje del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # 4. Iniciar la redacción de la IA
    with st.chat_message("assistant"):
        with st.spinner("🧠 Analizando datos y redactando informe ejecutivo..."):
            
            try:
                # Obtenemos la clave directamente (asegurate de que se llame GEMINI_API_KEY_1 en Secrets)
                clave_google = st.secrets["GEMINI_API_KEY_1"]
                genai.configure(api_key=clave_google)
                
                # Usamos el modelo más estable y rápido disponible
                modelo = genai.GenerativeModel('gemini-1.5-flash')

                # --- INSTRUCCIÓN ESTRICTA PARA EL ASESOR POLÍTICO ---
                prompt_asesor = f"""
                Sos un Asesor Político y Técnico de primer nivel para la provincia de La Pampa.
                Regla de oro: NO INVENTES INFORMACIÓN, DATOS NI NÚMEROS. 
                Si te pregunto sobre un tema específico, respondé de forma directa, ejecutiva y estructurada (usando viñetas o negritas).
                
                Consulta del usuario: {prompt_usuario}
                """

                # Generar la respuesta
                respuesta = modelo.generate_content(prompt_asesor).text
                
                # Mostrar el resultado final
                st.markdown(respuesta)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

            except KeyError:
                st.error("❌ Error de configuración: No se encontró la clave secreta 'GEMINI_API_KEY_1' en Streamlit. Revisá la configuración de Secrets.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")
