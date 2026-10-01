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
# ... (A PARTIR DE ACÁ SIGUE TU CÓDIGO NORMAL CON st.session_state) ...
