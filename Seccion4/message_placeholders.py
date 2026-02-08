# El fin de este script es demostrar cómo usar `MessagesPlaceholder` en un `ChatPromptTemplate` para mantener el contexto de una conversación. 
# En este ejemplo, se simula un historial de conversación entre un usuario y una IA, y luego se formatea un nuevo mensaje que incluye ese historial 
# para proporcionar contexto a la pregunta actual del usuario.

from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "Usuario: {pregunta_actual}")
])

# Simulamos un historial de conversación
historial_conversacion = [
    HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
    AIMessage(content="IA: La capital de Francia es París."),
    HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
    AIMessage(content="IA: París tiene aproximadamente 2.2 millones de habitantes en la ciudad propiamente dicha.")
]

mensajes = chat_prompt.format_messages(
    historial=historial_conversacion,
    pregunta_actual="¿Puedes decirme algo interesante de su arquitectura?"
)

for m in mensajes:
    print(m.content)