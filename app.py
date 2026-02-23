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

uploaded_files = st.file_uploader(
    "Sube tus documentos",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:

    all_text = ""

    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            all_text += read_pdf(uploaded_file)
        else:
            all_text += read_docx(uploaded_file)

    st.success("Documentos cargados correctamente")

    option = st.radio(
        "¿Qué quieres hacer?",
        ["📝 Generar preguntas", "💬 Chatear con los documentos"]
    )

    if option == "📝 Generar preguntas":
        if st.button("Crear preguntas"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un experto generador de preguntas tipo examen universitario."},
                    {"role": "user", "content": f"Genera 10 preguntas difíciles del siguiente texto:\n{all_text}"}
                ]
            )
            st.write(response.choices[0].message.content)

    if option == "💬 Chatear con los documentos":
        pregunta = st.text_input("Haz una pregunta sobre los documentos")
        if pregunta:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Responde usando únicamente la información de los documentos proporcionados."},
                    {"role": "user", "content": f"Documentos:\n{all_text}\n\nPregunta:\n{pregunta}"}
                ]
            )
            st.write(response.choices[0].message.content)
