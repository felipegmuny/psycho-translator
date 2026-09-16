import streamlit as st
from google import genai

st.set_page_config(page_title="Traductor Psicoeducativo", page_icon="🧠", layout="centered")

st.title("🧠 Traductor Psicoeducativo")
st.write("¡Épale! Pega aquí cualquier abstracto o artículo científico y te saco la idea clave, por qué importa en el día a día y los pasos prácticos para aplicarlo.")

# Retrieve API key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta la clave GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

user_text = st.text_area("Texto o abstracto científico (cualquier idioma):", height=200)

if st.button("Transformar a Folleto", type="primary"):
    if user_text.strip():
        prompt = f"""
        Eres un especialista en comunicación clínica y psicoeducación con un estilo súper cercano, cálido y con la forma de hablar típica de Venezuela. No importa en qué idioma esté el texto de entrada, tu tarea es procesarlo y redactar el resultado final siempre en un español venezolano natural y accesible.

        Responde exactamente con la siguiente estructura:

        📌 La Jugada Clave
        [Explica el hallazgo principal en 2 oraciones sencillas, humanas y sin enredos técnicos.]

        🧠 Por Qué Importa
        [Explica en 2-3 oraciones cómo se conecta esto con el día a día, la tranquilidad mental o el bienestar.]

        🛠️ Pasos Prácticos (A ponerse las pilas)
        1. [Estrategia accionable o pregunta de reflexión planteada de forma amigable.]
        2. [Estrategia accionable o pregunta de reflexión planteada de forma amigable.]

        Texto a procesar:
        {user_text}
        """
        with st.spinner("Traduciendo y adaptando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor pega un texto antes de continuar.")
