import os # Proporciona funciones para interactuar con el sistema operativo
from dotenv import load_dotenv # Carga variables de entorno desde un archivo .env
from langchain_openai import ChatOpenAI # Integración para interactuar con modelos de chat de OpenAI
from langchain.messages import AIMessage # Clase para representar mensajes generados por la IA
from langchain.messages import HumanMessage # Clase para representar mensajes enviados por el usuario
from langchain.messages import SystemMessage # Clase para definir el comportamiento base del sistema
import streamlit as st # Framework para la creación de interfaces web de ciencia de datos y ML

def configurar_entorno():
    """
    Carga las configuraciones de entorno y la API Key necesaria para OpenAI.
    
    Returns:
        str: La clave de API de OpenAI recuperada de las variables de entorno.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

# --- Configuración Inicial ---
OPENAI_API_KEY = configurar_entorno()

# Configuración de los metadatos de la página en el navegador
st.set_page_config(page_title="Chat de Yago", page_icon="😈")
st.title("Chat de Yago usando langchain")
st.markdown("Este es un pequeño ejemplo de un chat con langchain en streamlit")

# --- Instanciación del Modelo ---
# Se utiliza el modelo gpt-5-nano para procesar las peticiones.
# El parámetro temperature=0.0 asegura respuestas deterministas y técnicas.
chat_model = ChatOpenAI(
    model="gpt-5-nano-2025-08-07", 
    temperature=0.0, 
    api_key=OPENAI_API_KEY
)

# --- Gestión de Memoria y Estado de Sesión ---
# Se inicializa el historial de mensajes en la sesión de Streamlit si no existe.
# Esto evita que la conversación se reinicie cada vez que el script se vuelve a ejecutar.
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- Renderizado del Historial ---
# Itera sobre los mensajes almacenados para mostrarlos en la interfaz.
for msg in st.session_state.mensajes:
    # Los mensajes de sistema se omiten en la interfaz visual por ser instrucciones internas.
    if isinstance(msg, SystemMessage):
        continue
    
    # Determinación del rol basado en el tipo de objeto de LangChain
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    
    with st.chat_message(role):
        st.markdown(msg.content)

# --- Ciclo de Interacción de Usuario ---
# Captura la entrada del usuario mediante un cuadro de chat.
pregunta = st.chat_input("Escribe tu pregunta aquí: ")

if pregunta:
    # 1. Visualización inmediata del mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
        
    # 2. Persistencia: Se añade el mensaje humano al historial
    # Tipo: HumanMessage
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
    # 3. Inferencia: El modelo procesa toda la lista de mensajes (memoria)
    # Args: st.session_state.mensajes (list[BaseMessage])
    respuesta = chat_model.invoke(st.session_state.mensajes)
    
    # 4. Persistencia: Se añade la respuesta de la IA al historial
    # Tipo: AIMessage
    st.session_state.mensajes.append(respuesta)

    # 5. Visualización: Se muestra la respuesta generada en la interfaz
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)