import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Pluma Dorada | IA", page_icon="✒️", layout="wide")

# Estilos CSS personalizados para que se vea profesional (fondo, botones)
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
            # Priorizamos modelos rápidos y creativos
            modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if "models/gemini-1.5-flash" in modelos: return "models/gemini-1.5-flash"
            if "models/gemini-1.5-flash-001" in modelos: return "models/gemini-1.5-flash-001"
            return modelos[0] if modelos else "models/gemini-pro"
        except: return "models/gemini-pro"

    model = genai.GenerativeModel(get_working_model())
except:
    st.error("⚠️ Error de conexión. Revisa tus Secrets.")
    st.stop()

# --- INTERFAZ ---
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2893/2893466.png", width=80)
    st.title("Pluma de Oro")
    st.caption("Tu editor literario personal.")
    
    st.markdown("---")
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
    st.info("💡 **Tip Pro:** Las frases cortas funcionan mejor. Ej: *'Él la miró y sonrió'*.")

with col2:
    texto_usuario = st.text_area(
        "Escribe tu borrador o frase común aquí:", 
        height=150, 
        placeholder="Ejemplo: Ella sentía que él le estaba mintiendo, pero no quería decir nada para no arruinar el momento."
    )

    if st.button("✨ CONVERTIR EN LITERATURA", type="primary"):
        if not texto_usuario:
            st.toast("⚠️ Por favor escribe algo primero.")
        else
