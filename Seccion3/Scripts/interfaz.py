# En este script debo de implementar las siguientes mejoras:
#     1. Sidebar de Configuración: Permitir al usuario ajustar la temperatura.
#     2. Streaming de Respuestas: Mostrar la respuesta del modelo palabra por palabra, como ChatGPT.
#     3. Botón de Nueva Conversación: Permitir al usuario limpiar el historial fácilmente.


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



st.title("Tarea de la sección 3: IAgo")


# Sidebar: ajuste de temperatura y botón para limpiar historial
with st.sidebar:
    st.title("Configuración")
    temperatura = st.slider(label="Temperatura", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

    if st.button("Nueva conversación"):
        st.session_state.messages = []
        st.rerun()

# Configuramos el modelo que vamos a usar
llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature = temperatura,
    api_key = OPENAI_API_KEY
)


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
    
    # 1. Muestra y guarda el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt)) # Antes esto era st.session_state.messages.append({"role": "user", "content": prompt})
    

    # 2. Encadena la plantilla con el LLM usando LCEL (plantilla → llm)
    chain = plantilla | llm



    # 3. Opción sin streaming: devuelve la respuesta completa de una sola vez
    # response = chain.invoke({"mensajes": st.session_state.messages, "pregunta": prompt})

    # with st.chat_message("assistant"):
    #     st.markdown(response.content)
    #     st.session_state.messages.append(AIMessage(content=response.content)) # Antes esto era st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    
    
    # 3. Genera la respuesta en streaming: muestra el texto conforme llega
    try:
        with st.chat_message("assistant"):
            placeholder = st.empty() # Aquí, reservamos un espacio, en dónde vamos a poner la respuesta del modelo
            full_response = ""
            
            for chunk in chain.stream({"mensajes": st.session_state.messages, "pregunta": prompt}):
                full_response += chunk.content
                placeholder.markdown(full_response)
            
            placeholder.markdown(full_response)
            
            # 4. Guardar la respuesta completa al historial
            st.session_state.messages.append(AIMessage(content=full_response))
            
    except:
        st.error("Ha ocurrido un error al generar la respuesta: {str(e)}.")
