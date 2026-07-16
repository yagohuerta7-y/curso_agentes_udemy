import streamlit as st

import os
from pathlib import Path

from config import DATA_DIR
from services.vdb import VDB

from prompts.prompt_asistente import crear_sistema_prompts

from langchain.messages import AIMessage
from langchain.messages import HumanMessage
from langchain.messages import SystemMessage

from services.credencials import Configuration 
from services.retrievers import Retrievers


def main():

    st.set_page_config(
        page_title='RAG-IAgo',
        page_icon=':jack_o_lantern:',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.title('RAG-IAgo :jack_o_lantern:')

    st.divider()

    subir_archivos, chat_ui, citas = st.columns(3)

    with subir_archivos:
        upload_file()

    with chat_ui:
        # st.markdown('Escribe tu mensaje')
        chat()

    with citas:
        render_citas()



    # === Funciones ===

def upload_file():
    '''
    Funcion del apartado de subida y procesamiento de datos
    '''
    st.header("📋 Datos de Entrada")

    # Instanciamos la clase de la base de datos vectorial
    vdb = VDB()

    archivos = st.file_uploader(
        label="Sube tus archivos",
        accept_multiple_files=True,
        type=["pdf"]
    )

    data_dir = DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)

    if archivos:
        for archivo in archivos:
            path = data_dir / archivo.name
            with open(path, "wb") as f:
                f.write(archivo.getbuffer())

        if st.button("Procesar datos"):
            vdb.carga_docs()
            vdb.chunking()
            vdb.creation()

        if st.button('Borrar datos'):
            # Borramos los documentos de la base de datos y los archivos de VDB
            vdb.delete()

            # Eliminamos fisicamente los archivos subidos
            for ruta in DATA_DIR.iterdir():
                if ruta.is_file():
                    ruta.unlink()

            # Limpiamos tambien las citas mostradas
            st.session_state.citas = []  # evitar referencias a fuentes borradas

    else:
        st.info("No se ha subido ningun archivo todavia.")




def render_citas():
    '''
    Renderiza la pestaña de citas en la tercera columna.
    Cada fuente (source + pagina) se muestra como un expander
    individual. Las mas recientes aparecen primero.
    '''
    st.header("📚 Citas")

    citas = st.session_state.get("citas", [])

    # Sin turnos previos: placeholder amigable
    if not citas:
        st.info("Aún no hay citas. Haz una pregunta para ver las fuentes.")
        return

    # Aplanamos turnos en una lista por fuente, conservando la query asociada
    flat = []
    for turno in reversed(citas):
        for f in turno.get("fuentes", []):
            flat.append({**f, "query": turno["query"]})

    # Un expander por fuente: nombre del PDF, pagina y preview al expandir
    for j, fuente in enumerate(flat, 1):
        source_path = fuente.get("source") or ""
        source_name = Path(source_path).name if source_path else "Desconocido"
        header = f"[{j}] {source_name} — pág. {fuente.get('page', '?')}"
        with st.expander(header):
            st.caption(f"Pregunta: {fuente['query']}")
            st.markdown(fuente.get("preview", ""))


def chat():
    '''
    Funcion para renderizar la seccion del chat
    '''

    configuration = Configuration()
    prompt = crear_sistema_prompts()


    # Configuramos el session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'citas' not in st.session_state:
        st.session_state.citas = []  # historial acumulado de fuentes por turno

    for message in st.session_state.messages:

        # Si es un mensaje del sistema, no lo mostramos
        if isinstance(message, SystemMessage):
            continue

        # Obtenemos el rol del mensaje y lo mostramos en la pagina
        role = 'assistant' if isinstance(message, AIMessage) else 'user'

        # Mostramos el mensaje
        with st.chat_message(role):
            st.markdown(message.content)


    # Hacemos la logica de los mensajes:
    if query := st.chat_input('¿En que te puedo ayudar hoy?'):

        # 1. Muestra y guarda el mensaje del usuario
        with st.chat_message('user'):
            st.markdown(query)
        st.session_state.messages.append(HumanMessage(content=query))

        # Inicializamos el retriver con la pregunta del usuario
        list_retrievers = Retrievers(query=query).Query()

        retrievers = (
            '\n\n'.join(d.page_content for d in list_retrievers)
            if list_retrievers
            else "No se encontró información relevante en la base de datos."
        )

# Guardamos metadata de cada fuente para la pestaña de citas
        # preview recortado a 300 chars para no saturar la UI ni session_state
        citas_turno = [
            {
                "source": d.metadata.get("source", "Desconocido"),
                "page": d.metadata.get("page", "?"),
                "preview": (d.page_content[:300] + "...") if len(d.page_content) > 300 else d.page_content,
            }
            for d in list_retrievers
        ]
        st.session_state.citas.append({"query": query, "fuentes": citas_turno})

        # 2. Encadena la plantilla con el llm 
        chain = prompt | configuration.llm_model

        # 3. Muestra la respuesta en streaming
        try:
            with st.chat_message('assistant'):
                placeholder = st.empty()
                full_response = ''

                # for chunk in chain.stream({'mensajes': st.session_state.messages, 'pregunta': query}):
                for chunk in chain.stream({'query': query, 'retrievers': retrievers}):
                    full_response += chunk.content
                    placeholder.markdown(full_response)

                placeholder.markdown(full_response)


                # 4. Guardar la respuesta completa en el historial
                st.session_state.messages.append(AIMessage(content=full_response))

        except Exception as e:
            st.error(f'Ha ocurrido un error: {e}')