import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Asesor Político - Audinos", page_icon="🇦🇷", layout="centered")

# 2. Encabezado personalizado con tu caricatura y nombre
col1, col2 = st.columns([1, 4])
with col1:
    # Busca tu imagen y la ajusta al tamaño ideal
    if os.path.exists("squat.png"):
        st.image("squat.png", width=120)
    else:
        st.write("🇦🇷") # Por si la imagen tarda en cargar

with col2:
    st.title("Hola, soy Audinos 👋")
    st.caption("📍 Santa Rosa, La Pampa")

st.markdown("""
Desarrollé este asistente de inteligencia artificial para agilizar nuestro trabajo técnico y político. 

Está configurado estrictamente con datos provinciales, leyes y presupuestos reales. Su regla principal es la precisión: **si la información no está en los documentos, no la inventa.** 

¿En qué te puedo ayudar hoy?
""")

# 3. Inicializar el historial de chat en la memoria de la página
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar el historial de mensajes al cargar la página
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 4. Caja de texto para que el usuario pregunte
prompt_usuario = st.chat_input("Escribí tu consulta política, presupuestaria o técnica...")

if prompt_usuario:
    # Mostrar el mensaje del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # 5. Iniciar la redacción de la IA con rotación de modelos
    with st.chat_message("assistant"):
        with st.spinner("🧠 Analizando datos y redactando informe..."):
            
            # Cargamos todas las claves que tengas en tus Secrets de Streamlit
            cuentas_keys = [
                st.secrets.get("GEMINI_API_KEY_1"),
                st.secrets.get("GEMINI_API_KEY_2"),
                st.secrets.get("GEMINI_API_KEY_3"),
                st.secrets.get("GEMINI_API_KEY_4")
            ]
            
            # Lista de modelos (Intentará usar el primero, si falla pasa al segundo)
            modelos_disponibles = [
                'gemini-3.8-flash', 
                'gemini-3.7-flash',
                'gemini-3.6-flash',
                'gemini-3.5-flash',
                'gemini-3.1-flash-lite',
                'gemini-2.5-flash',
                'gemini-1.5-flash'
            ]
            
            respuesta = None
            ultimo_error = None

            # --- INSTRUCCIÓN ESTRICTA PARA EL ASESOR POLÍTICO ---
            prompt_asesor = f"""
            Sos un Asesor Político y Técnico de primer nivel para la provincia de La Pampa.
            Regla de oro: NO INVENTES INFORMACIÓN, DATOS NI NÚMEROS. 
            Si te pregunto sobre un tema específico, respondé de forma directa, ejecutiva y estructurada (usando viñetas o negritas).
            
            Consulta del usuario: {prompt_usuario}
            """

            # Bucle 1: Recorrer las claves API
            for key in cuentas_keys:
                if not key:
                    continue # Si la clave está vacía, pasa a la siguiente
                    
                try:
                    genai.configure(api_key=key)
                    
                    # Bucle 2: Recorrer los modelos
                    for nombre_modelo in modelos_disponibles:
                        try:
                            temp_model = genai.GenerativeModel(nombre_modelo)
                            # Intentamos generar la respuesta
                            respuesta = temp_model.generate_content(prompt_asesor).text
                            break # ¡ÉXITO! Rompemos el bucle de modelos
                            
                        except Exception as e:
                            ultimo_error = e
                            continue # FALLÓ ESTE MODELO, pasa al siguiente
                            
                    if respuesta:
                        break # ¡ÉXITO! Ya tenemos respuesta, salimos de las claves
                        
                except Exception as e:
                    ultimo_error = e
                    continue # FALLÓ LA CLAVE COMPLETA, pasa a la siguiente

            # 6. Mostrar el resultado final en la pantalla
            if respuesta:
                st.markdown(respuesta)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            else:
                # Si fallaron TODAS las claves y TODOS los modelos
                if ultimo_error and ("429" in str(ultimo_error) or "Quota" in str(ultimo_error)):
                    st.warning("⚠️ Hay demasiadas consultas en simultáneo. Esperá un minuto y volvé a intentar.")
                elif ultimo_error and "API_KEY_INVALID" in str(ultimo_error):
                    st.error("❌ Error: La clave de Google (API Key) es inválida o no está bien configurada en los Secrets.")
                else:
                    st.error(f"❌ Error técnico general: {ultimo_error}")
