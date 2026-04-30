# MessagesPlaceholder es un componente que va dentro de un ChatPromptTemplate y reserva un espacio para insertar una lista completa de mensajes en una posición específica del prompt.
# Sin MessagesPlaceholder, si quisieras meter el historial de conversación en un ChatPromptTemplate, tendrías que convertirlo manualmente a un string y perderías los roles
# Además, otro caso de uso sumamente útil, es que se puede usar

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

# Hacemos el template para que ya contemple el historial de mensajes
chat_prompt = ChatPromptTemplate(
    [
        ("system", "Eres un asistente que ayudará al usuario en lo que te pida"),
        MessagesPlaceholder(variable_name="historial"),
        ("human", "{pregunta_actual}")
    ]
)

# Simulamos un historial de conversación
historial_conversacion = [
    HumanMessage(content="¿Cuál es la capital de Francia?"),
    AIMessage(content="La capital de Francia es París"),
    HumanMessage(content="¿Cuantos habitantes tiene?"),
    AIMessage(content="Tiene una población de aproximadamente de 2.2 millones de habitantes")
]

# Hacemos una prueba de formato para ver como salen los mensajes
mensajes = chat_prompt.format_messages(
    historial = historial_conversacion,
    pregunta_actual = "Dime cual fue el mejor matemático de la historia de Francia"
)

for mensaje in mensajes:
    print(mensaje.content)