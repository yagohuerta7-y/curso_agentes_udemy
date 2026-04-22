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
    # Si no hay mensajes en el session state, inicializamos la conversación con un mensaje del sistema
    st.session_state.messages = [
        SystemMessage(content="Eres un asistente llamado IAgo, responde a las preguntas que te haga el usuario.")
    ]
    

# Hacemos el prompt template
plantilla = PromptTemplate(
    input_variables = ["mensajes", "pregunta"],
    template = """
    El historial de la conversación es el siguiente:
    {mensajes}
    
    La pregunta del usuario es esta:
    {pregunta}
    """
)


# Mostramos los mensajes en la página
for message in st.session_state.messages:
    
    # Si es un mensaje del sistema, no lo mostramos 
    if isinstance(message, SystemMessage):
        continue
    
    # Obtenemos el rol del mensaje (assistant o user) y lo mostramos en la página
    role = "assistant" if isinstance(message, AIMessage) else "user"
    
    # Mostramos el mensaje
    with st.chat_message(role):
        st.markdown(message.content)
        
        
        
# Hacemos la lógica de los mensajes
if prompt := st.chat_input("¿En que te puedo ayudar hoy?"):
    
    # 1. Mostramos el mensaje que puso el usuario y lo guardamos en el session state
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append(HumanMessage(content=prompt)) # Antes esto era st.session_state.messages.append({"role": "user", "content": prompt})
    

    # 2. Hacemos la cadena (solo cuando hay un mensaje de parte del usuario)
    chain = plantilla | llm

    # 3. Generamos la respuesta
    response = chain.invoke({"mensajes": st.session_state.messages, "pregunta": prompt})

    # 4. Mostramos y guardamos la respuesta del modelo
    with st.chat_message("assistant"):
        st.markdown(response.content)
        st.session_state.messages.append(AIMessage(content=response.content)) # Antes esto era st.session_state.messages.append({"role": "assistant", "content": response.content})