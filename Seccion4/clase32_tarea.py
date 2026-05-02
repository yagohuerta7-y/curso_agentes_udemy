# En esta tarea transformarás tu chatbot del tema anterior para usar ChatPromptTemplate en lugar de PromptTemplate. 
# Descubrirás las ventajas de trabajar con templates diseñados específicamente para modelos de chat y cómo estructurar prompts de forma más clara y eficiente.
# En el código original del proyecto de la sección 3 ya hacía una separación de los mensajes usando las clases de AIMessage, HumanMessage y SystemMessage
# así que ahora lo voy a cambiar para usar ChatPromptTemplate
# Nota: Agregué el historial usando la clase 'MessagesPlaceholder', no estaba en el ejercicio de la unidad, pero fue un extra mio.




import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
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
    
    # NUEVO: Agregamos el rol/personalidad/tono al modelo
    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )
    

    if st.button("Nueva conversación"):
        st.session_state.messages = []
        st.rerun()

# Configuramos el modelo que vamos a usar
llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature = temperatura,
    api_key = OPENAI_API_KEY
)


# NUEVO: Hacemos el template dinámico del rol/personalidad/tono
system_messages = {
    "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
    "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
    "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
    "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
    "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
}


# Configuramos el session state (para guardar el historia en una especie de caché)
if "messages" not in st.session_state:
    st.session_state.messages = []
    

# NUEVO: Hacemos el prompt template
chat_prompt = ChatPromptTemplate.from_messages(
    [
            # Definimos la personalidad del asistente con un system message
            ("system", system_messages[personalidad]),
            
            # Aquí ponemos el historial del chat
            MessagesPlaceholder(variable_name="mensajes"),
            
            # Ponemos la pregunta actual
            ("human", "La pregunta del usuario es esta: \n {pregunta}")
    ]
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
    chain = chat_prompt | llm  
    
    
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