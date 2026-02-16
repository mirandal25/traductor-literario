import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="La Pluma de Oro | IA", page_icon="✒️", layout="wide")

# Estilos CSS
st.markdown("""
<style>
    .stTextArea textarea {font-size: 16px !important;}
    .stButton button {width: 100%; border-radius: 5px; font-weight: bold;}
    div[data-testid="stExpander"] {border: none; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE IA (Auto-Detect) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    def get_working_model():
        try:
            modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Prioridad al modelo Flash (rápido y gratis)
            if "models/gemini-1.5-flash" in modelos: return "models/gemini-1.5-flash"
            if "models/gemini-1.5-flash-001" in modelos: return "models/gemini-1.5-flash-001"
            return modelos[0] if modelos else "models/gemini-pro"
        except: 
            return "models/gemini-pro"

    nombre_modelo = get_working_model()
    model = genai.GenerativeModel(nombre_modelo)
except:
    st.error("⚠️ Error de conexión con Google. Revisa tus Secrets.")
    st.stop()

# --- INTERFAZ ---
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2893/2893466.png", width=80)
    st.title("Pluma de Oro")
    st.caption("Tu editor literario personal.")
    
    st.markdown("---") # BOTÓN DE MONETIZACIÓN
    st.markdown("### ☕ Apoya este proyecto")
    st.write("¿Te ayudé a escribir tu escena? Ayúdame a mantener la IA activa.")
    st.link_button("Invítame un Café ($3 USD)", "https://ko-fi.com/mirandal")
    genero = st.selectbox(
        "📂 Género Literario:",
        ["Romance Oscuro", "Erótico/Spicy", "Drama Psicológico", "Fantasía Épica", "Terror Lovecraftiano", "Poesía Trágica"]
    )
    
    tono = st.select_slider(
        "🎚️ Nivel de Intensidad:",
        options=["Sutil", "Moderado", "Intenso", "Visceral"],
        value="Moderado"
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Las frases cortas funcionan mejor. Ej: *'Él la miró y sonrió'*.")

with col2:
    texto_usuario = st.text_area(
        "Escribe tu borrador o frase común aquí:", 
        height=150, 
        placeholder="Ejemplo: Ella sentía que él le estaba mintiendo, pero no quería decir nada para no arruinar el momento."
    )

    if st.button("✨ CONVERTIR EN LITERATURA", type="primary"):
        if not texto_usuario:
            st.warning("⚠️ Por favor escribe algo primero.")
        else:
            # AQUÍ ESTABA EL ERROR, YA CORREGIDO CON LOS DOS PUNTOS:
            with st.spinner('La IA está puliendo tu prosa...'):
                try:
                    prompt = f"""
                    Actúa como un autor best-seller de {genero}. Tu objetivo es reescribir el siguiente texto plano para que sea digno de publicar en un libro físico.
                    
                    Texto original: "{texto_usuario}"
                    
                    Instrucciones:
                    1. Tono: {tono}.
                    2. Muestra, no cuentes (Show, don't tell). Usa metáforas sensoriales.
                    3. Si es Romance Oscuro/Erótico, enfócate en la tensión física y psicológica.
                    4. Genera EXACTAMENTE 3 opciones distintas:
                       - Opción 1: Elegante y directa.
                       - Opción 2: Poética y metafórica.
                       - Opción 3: Intensa y emocional (la mejor para momentos climáticos).
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.success("✅ Traducción completada")
                    st.markdown("### 🖋️ Tus Opciones:")
                    st.text_area("Copia tus resultados aquí:", value=response.text, height=400)
                    
                except Exception as e:
                    st.error(f"Error técnico: {e}")

# Pie de página
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Herramienta exclusiva v2.1</div>", unsafe_allow_html=True)
