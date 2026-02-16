import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Traductor Literario IA", page_icon="✒️", layout="centered")

# Título y Subtítulo
st.title("✒️ La Pluma de Oro")
st.subheader("Transforma tus borradores en literatura de alto nivel")

# Configuración de la API (Se conecta con el secreto)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Error: No se encontró la clave API. Configúrala en los secrets de Streamlit.")

# Menú lateral
with st.sidebar:
    st.header("Configuración")
    genero = st.selectbox(
        "Selecciona el Género Literario:",
        ["Romance Oscuro", "Fantasía Épica", "Terror Lovecraftiano", "Novela Negra", "Poesía Melancólica", "Realismo Mágico"]
    )
    intensidad = st.slider("Nivel de intensidad literaria:", 1, 3, 2)
    st.info("💡 Consejo: Sé específico con tu frase original.")

# Área de entrada
texto_usuario = st.text_area("Escribe tu frase común aquí (ej: 'El entró al cuarto y la miró con odio'):", height=100)

# Botón de acción
if st.button("✨ Traducir a Literatura"):
    if not texto_usuario:
        st.warning("Por favor, escribe una frase primero.")
    else:
        with st.spinner('La IA está reescribiendo tu texto...'):
            try:
                # El Prompt maestro (La instrucción secreta)
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""
                Actúa como un escritor bestseller experto en el género {genero}.
                Tu tarea es reescribir la siguiente frase común: "{texto_usuario}".
                
                Reglas:
                1. Usa vocabulario avanzado y sensorial propio del {genero}.
                2. Nivel de intensidad: {intensidad}/3.
                3. No des explicaciones, solo entrega 3 opciones diferentes de la frase reescrita.
                4. Si el género es Romance Oscuro, enfócate en la tensión, la posesión y las emociones viscerales.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Aquí tienes tus opciones:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# Pie de página
st.markdown("---")
st.caption("Herramienta creada para escritores profesionales.")
