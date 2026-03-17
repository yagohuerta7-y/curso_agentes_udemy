import os # Proporciona funciones para interactuar con el sistema operativo
from dotenv import load_dotenv # Carga variables de entorno desde un archivo .env
from langchain_openai import ChatOpenAI # Integración para interactuar con modelos de chat de OpenAI
from langchain.messages import AIMessage # Clase para representar mensajes generados por la IA
from langchain.messages import HumanMessage # Clase para representar mensajes enviados por el usuario
from langchain.messages import SystemMessage # Clase para definir el comportamiento base del sistema
from langchain_core.prompts import PromptTemplate # Clase para crear plantillas de prompts
import streamlit as st # Framework para la creación de interfaces web de ciencia de datos y ML


def carga_credenciales():
    """
    Función que carga de manera automática la api de OpenAI
    """
    
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


# --- Configuración inicial ---
OPEN_AI_API_KEY = carga_credenciales()


# --- Datos de la página ---
st.set_page_config(page_title="Chat de Yago", page_icon="😈")
st.title("Chat de la tarea del curso de udemy")


# --- Configuración del modelo con el panel lateral ---
with st.sidebar:
    st.header("Configuración del modelo")
    temperatura = st.slider(label="Temperatura", min_value=0.0, max_value=1.0, step=0.1)
    model_name = st.selectbox(label="Modelo", options=["gpt-5-nano-2025-08-07", "gpt-5-mini-2025-08-07"])
    
    # Botón para reiniciar la conversación
    if st.button("Nueva conversación"):
        st.session_state.mensajes = []
        st.rerun()
    

# --- Gestión de la memoria ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    




# Definimos el modelo 
model = ChatOpenAI(
    model = model_name,
    temperature=temperatura,
    api_key=OPEN_AI_API_KEY
)


# Definimos la plannntilla del prompt
plantilla = PromptTemplate(
    input_variables = ["mensaje", "historial"],
    template = """
    # Rol: Eres un asistente experto, útil, y preciso.
    
    Historial de la conversación:
    {historial}
    
    Responde a esta pregunta de forma concisa:
    {mensaje}
    """
)

chain = plantilla | model


# --- Renderizado del historial ---
for msg in st.session_state.mensajes:
    # Si es el sistem instruction, no mostramos nada
    if isinstance(msg, SystemMessage):
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)


# --- Interacción con el usuario ---
if prompt := st.chat_input("Escribe tu mensaje..."):
    # 1. Mostrar y guardar mensaje del usuario
    st.session_state.mensajes.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Pasamos el historial como contexto (excluyendo el mensaje actual para no duplicar lógica si fuera necesario, 
        # pero aquí pasamos todo el estado actual como historial para que tenga contexto)
        for chunk in chain.stream({"mensaje": prompt, "historial": st.session_state.mensajes}):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # 3. Guardar respuesta del asistente
    st.session_state.mensajes.append(AIMessage(content=full_response))
        
