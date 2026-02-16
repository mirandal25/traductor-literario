import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Pluma de Oro", page_icon="✒️", layout="centered")
st.title("✒️ La Pluma de Oro")
st.caption("Herramienta de Traducción Literaria con IA")

# --- CONEXIÓN Y BUSCADOR DE MODELOS ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Esta función busca qué modelo tienes disponible automáticamente
    def get_working_model():
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    if 'gemini' in m.name:
                        return m.name
            return "models/gemini-pro" # Respaldo
        except:
            return "models/gemini-pro"

    modelo_detectado = get_working_model()
    # Mostramos qué cerebro encontró (para que sepas que funcionó)
    st.sidebar.success(f"🟢 Conectado a: {modelo_detectado.replace('models/', '')}")
    model = genai.GenerativeModel(modelo_detectado)

except Exception as e:
    st.error("⚠️ Error de Conexión. Revisa tu API Key en los Secrets.")
    st.stop()

# --- INTERFAZ ---
with st.sidebar:
    st.header("Configuración")
    genero = st.selectbox(
        "Estilo Literario:",
        ["Romance Oscuro", "Fantasía Épica", "Terror Psicológico", "Realismo Sucio", "Poesía Gótica"]
    )
    intensidad = st.slider("Nivel de Intensidad:", 1, 3, 3)

# --- ÁREA DE TRABAJO ---
texto_usuario = st.text_area("Escribe tu frase aquí:", height=100, placeholder="Ej: Él entró a la habitación y la miró fijamente.")

if st.button("✨ Traducir Texto"):
    if not texto_usuario:
        st.warning("Escribe algo para traducir.")
    else:
        with st.spinner('Reescribiendo...'):
            try:
                prompt = f"""
                Actúa como un escritor bestseller de {genero}.
                Reescribe esta frase: "{texto_usuario}".
                
                Reglas:
                1. Tono: {genero}.
                2. Intensidad: {intensidad}/3.
                3. Dame 3 variaciones distintas.
                4. No expliques nada, solo dame las frases.
                """
                
                response = model.generate_content(prompt)
                st.markdown("### Resultados:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
