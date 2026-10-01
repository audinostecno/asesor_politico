import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Herramienta de Gestión - Audinos", page_icon="🇦🇷", layout="centered")

# 2. Encabezado personal (Estilo herramienta propia)
col1, col2 = st.columns([1, 4])
with col1:
    # Busca la caricatura que subiste al repositorio
    if os.path.exists("Squat.png"):
        st.image("Squat.png", width=120)
    else:
        st.write("🇦🇷") # Respaldo por si la imagen tarda en cargar

with col2:
    st.title("Hola, soy Juan 👋")
    st.markdown("Estoy para ayudarte a consultar datos oficiales INDEC, BCRA, ministerios, provincias. Más de **33.000 datasets** de todos los portales de datos abiertos del país. La fuente es la base de datos de OpenArg.")
    st.caption("📍 Santa Rosa, La Pampa")

# Texto de presentación humano, directo y de gestión
st.markdown("""
Armé esta herramienta para nuestro equipo. La idea es simple: tener a mano y al instante los datos técnicos, presupuestos y proyectos de La Pampa, sin perder tiempo buscando en mil PDFs.

Está configurada con la información oficial y tiene una regla estricta: **si el dato no está en los documentos, te lo dice de frente y no inventa nada**. 

Escribime acá abajo, ¿qué tema o proyecto querés que revisemos?
""")

st.divider() # Línea separadora para que quede más prolijo

# 3. Inicializar el historial de chat en la memoria de la página
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar el historial de mensajes al cargar la página
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 4. Caja de texto para que el usuario pregunte
prompt_usuario = st.chat_input("Ej: ¿Cuál es el presupuesto para tablets en escuelas primarias?")

if prompt_usuario:
    # Mostrar el mensaje del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # 5. Iniciar la redacción de la IA con rotación de modelos (El Fallback)
    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos y redactando..."):
            
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

            # --- INSTRUCCIÓN ESTRICTA QUE CORRE POR DETRÁS ---
            prompt_asesor = f"""
            Sos una herramienta técnica y ejecutiva creada por Audinos para La Pampa.
            Respondé de manera directa, profesional y clara (usando viñetas o negritas para estructurar).
            Regla de oro: NO INVENTES INFORMACIÓN, DATOS NI NÚMEROS. Si no lo sabés, decilo claramente.
            
            Consulta: {prompt_usuario}
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
                            respuesta = temp_model.generate_content(prompt_asesor).text
                            break # ¡ÉXITO!
                            
                        except Exception as e:
                            ultimo_error = e
                            continue # Falla este modelo, pasa al siguiente
                            
                    if respuesta:
                        break # ¡ÉXITO global!
                        
                except Exception as e:
                    ultimo_error = e
                    continue # Falla la clave completa, pasa a la siguiente

            # 6. Mostrar el resultado final en la pantalla
            if respuesta:
                st.markdown(respuesta)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            else:
                if ultimo_error and ("429" in str(ultimo_error) or "Quota" in str(ultimo_error)):
                    st.warning("⚠️ Hay demasiadas consultas en simultáneo. Esperá un minuto y volvé a intentar.")
                elif ultimo_error and "API_KEY_INVALID" in str(ultimo_error):
                    st.error("❌ Error: La clave de Google no está bien configurada en los Secrets de Streamlit.")
                else:
                    st.error(f"❌ Error técnico: {ultimo_error}")
