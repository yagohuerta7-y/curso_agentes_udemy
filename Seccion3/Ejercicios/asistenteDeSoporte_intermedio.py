# Objetivo: Utilizar ChatPromptTemplate para estructurar una conversación profesional.

#     * Instrucciones: 
        
#         ** Crea un SystemMessagePromptTemplate que defina al IA como un experto en ciberseguridad.

#         ** Crea un HumanMessagePromptTemplate que reciba una variable llamada incidente.

#         ** Combínalos en un ChatPromptTemplate.

# Pista: Recuerda que en LangChain para chats, el orden de los mensajes importa para el contexto.



# --- Importamos las dependencias ---

import os # Para manejar el sistema operativo
from dotenv import load_dotenv # Para cargar las variables de entorno
from langchain_openai import ChatOpenAI # Para interactuar con el modelo de OpenAI  
from langchain.messages import AIMessage # Para representar mensajes generados por la IA
from langchain.messages import HumanMessage # Para representar mensajes enviados por el usuario
from langchain.messages import SystemMessage # Para definir el comportamiento base del sistema
from langchain_core.prompts import ChatPromptTemplate # Para crear plantillas de prompts específicas para chats
from langchain_core.prompts import MessagesPlaceholder # Para incluir un marcador de posición para mensajes dinámicos en la plantilla de chat



# --- Configuraciones ---

# Cargamos las variables de entorno
load_dotenv()

# Guardamos la API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el LLM
llm = ChatOpenAI(
    model="gpt-5-nano-2025-08-07", 
    temperature=0.0, 
    api_key=OPENAI_API_KEY
    )



# --- Plantillas e historial ---

# Definimos en dónde vamos a guardar los mensajes
chat_history = []

# Definimos la platilla del chat
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un experto en ciberseguridad, que respoderá las preguntas del usuario"),
        MessagesPlaceholder(variable_name="chat_history"), # Inyectamos el historial de mensajes aquí
        ("human", "{pregunta}")
    ]
)

# Aquí, vamos a guardar la pregunta del usuario
pregunta = ""

# Definimos la cadena de la respuesta
chain = prompt | llm



# ---  Bucle para chatear ---

while pregunta != "salir":
    
    # El usuario escribe su pregunta
    pregunta = input("Introduce tu pregunta (o 'salir' para terminar): ")
    
    
    # Invocamos la respuesta del modelo
    respuesta = chain.invoke(
        {
            "pregunta": pregunta, # Asociamos la pregunta del usuario con la variable
            "chat_history": chat_history # Inyectamos el historial de mensajes en la plantilla
        }
    )
    
    # Guardamos el historial
    chat_history.append(HumanMessage(content=pregunta))
    print(f"Respuesta: {respuesta.content}")
    chat_history.append(respuesta)
    

