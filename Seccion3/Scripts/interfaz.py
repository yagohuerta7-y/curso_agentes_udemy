import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.messages import AIMessage
from langchain.messages import HumanMessage
from langchain.messages import SystemMessage


# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuramos el modelo que vamos a usar
llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature = 0.0,
    api_key = OPENAI_API_KEY
)



st.title("Tarea de la sección 3: IAgo")


# Configuramos el session state (para guardar el historia en una especie de caché)
if "messages" not in st.session_state:
    st.session_state.messages = []
    

# Hacemos el prompt template
plantilla = PromptTemplate(
    input_variables = ["mensajes", "pregunta"],
    template = """
    Eres un asistente llamado IAgo, responde a las preguntas que te haga el usuario.
    El historial de la conversación es el siguiente:
    {mensajes}
    
    La pregunta del usuario es esta:
    {pregunta}
    """
)


# Mostramos los mensajes en la página
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        
# Hacemos la lógica de los mensajes
if prompt := st.chat_input("¿En que te puedo ayudar hoy?"):
    
    # 1. Mostramos el mensaje que puso el usuario
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Añadimos el mensaje del usuario al historial del chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    # 3. Hacemos la cadena (solo cuando hay un mensaje de parte del usuario)
    chain = plantilla | llm

    # 4. Generamos la respuesta
    response = chain.invoke({"mensajes": st.session_state.messages, "pregunta": prompt})

    # 5. Mostramos y guardamos la respuesta del modelo
    with st.chat_message("assistant"):
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})