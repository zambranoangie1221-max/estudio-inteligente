import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from openai import OpenAI

st.set_page_config(page_title="Estudio Inteligente", layout="centered")

st.title("📚 Asistente de Estudio Personal")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

uploaded_file = st.file_uploader("Sube tu documento", type=["pdf", "docx"])

if uploaded_file:

    if uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    else:
        text = read_docx(uploaded_file)

    st.success("Documento cargado correctamente")

    option = st.radio(
        "¿Qué quieres hacer?",
        ["📝 Generar preguntas", "💬 Chatear con el documento"]
    )

    if option == "📝 Generar preguntas":
        dificultad = st.selectbox("Nivel de dificultad", ["Fácil", "Intermedio", "Difícil"])
        
        if st.button("Crear preguntas"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un experto generador de preguntas tipo examen universitario."},
                    {"role": "user", "content": f"Genera 10 preguntas nivel {dificultad} del siguiente texto:\n{text}"}
                ]
            )
            st.write(response.choices[0].message.content)

    if option == "💬 Chatear con el documento":
        pregunta = st.text_input("Haz una pregunta sobre el documento")

        if pregunta:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Responde usando únicamente la información del documento proporcionado."},
                    {"role": "user", "content": f"Documento:\n{text}\n\nPregunta:\n{pregunta}"}
                ]
            )
            st.write(response.choices[0].message.content)
