# El ChatPromptTemplate genera una lista de mensajes estructurados con roles (system, human, assistant).
# Esta clase es la ideal para cuando tienes una aplicación conversacional, o en general, en dónde el modelo
# necesita saber su rol o tener instrucciones de comportamiento.

from langchain_core.prompts import ChatPromptTemplate

# Hacemos el template de los mensajes, pero ya incluyendo los roles
chat_prompt = ChatPromptTemplate(
    [
        ("system", "Eres un traductor del español al inglés muy preciso."),
        ("human", "{texto}")
    ]
)

# Para poder ver cómo se estructura, lo probamos
mensajes = chat_prompt.format_messages(texto = "Hola mundo, ¿Cómo estás?")

# Recorremos la lista de mensajes
for mensaje in mensajes:
    print(f"{type(mensaje)}: {mensaje}")
    
    
# Esto es lo que se retorna:
# <class 'langchain_core.messages.system.SystemMessage'>: content='Eres un traductor del español al inglés muy preciso.' additional_kwargs={} response_metadata={}
# <class 'langchain_core.messages.human.HumanMessage'>: content='Hola mundo, ¿Cómo estás?' additional_kwargs={} response_metadata={}

# Esto ya tiene los roles bien definidos