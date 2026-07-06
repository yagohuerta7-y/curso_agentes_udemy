import streamlit as st
import os
from services.cv_minsait_extract import extraer
from services.generar_pptx import generar_pptx

PLANTILLA_PATH = os.path.join(os.path.dirname(__file__), "..", "plantilla.pptx")


def main():
    st.set_page_config(
        page_title="CV Minsait",
        page_icon=":briefcase:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("CV formato Minsait :briefcase:")

    if "cv_data" not in st.session_state:
        st.session_state.cv_data = None

    with st.container(border=True):
        procesar_archivo()



def procesar_archivo():
    archivo_cv = st.file_uploader(
        label='Introduce el cv del candidato',
        type=['pdf', 'docx'],
        help='Selecciona un archivo PDF o DOCX que contenga el currículum del candidato'
    )

    if archivo_cv is not None:
        st.success(f"Archivo cargado: {archivo_cv.name}")

    if st.button(label='Procesar'):
        if archivo_cv is not None:
            resultado = extraer(archivo_cv)
            if isinstance(resultado, str) and resultado.startswith("Error"):
                st.error(resultado)
            else:
                st.session_state.cv_data = resultado
                st.json(resultado)
        else:
            st.warning("Por favor, sube un archivo antes de procesar.")

    if st.session_state.cv_data is not None:
        st.divider()
        if st.button(label='Generar y Descargar PPTX'):
            with st.spinner("Generando PPTX..."):
                output_path = os.path.join(os.path.dirname(__file__), "..", "output.pptx")
                generar_pptx(st.session_state.cv_data, PLANTILLA_PATH, output_path)
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="Descargar output.pptx",
                        data=f,
                        file_name="output.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
