if prompt_usuario:
    # 1. Mostrar la pregunta del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # 2. Iniciar la redacción de la IA
    with st.chat_message("assistant"):
        with st.spinner("🧠 Analizando datos y redactando informe ejecutivo..."):
            
            # Cargamos todas las claves que tengas en tus Secrets de Streamlit
            cuentas_keys = [
                st.secrets.get("GEMINI_API_KEY_1"),
                st.secrets.get("GEMINI_API_KEY_2"),
                st.secrets.get("GEMINI_API_KEY_3"),
                st.secrets.get("GEMINI_API_KEY_4")
            ]
            
            # Lista de modelos (Intentará usar el primero, si falla pasa al segundo)
            # Agregamos 'gemini-1.5-flash' al final como último salvavidas estándar
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
            Sos un Asesor Político y Técnico de primer nivel.
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
                            # Usamos el prompt del asesor en lugar del pedagógico
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

            # 3. Mostrar el resultado final en la pantalla
            if respuesta:
                st.markdown(respuesta)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            else:
                # Si fallaron TODAS las claves y TODOS los modelos
                if ultimo_error and ("429" in str(ultimo_error) or "Quota" in str(ultimo_error)):
                    st.warning("⚠️ Hay demasiadas consultas en simultáneo. Esperá un minuto y volvé a intentar.")
                else:
                    st.error(f"❌ Error técnico general: {ultimo_error}")
