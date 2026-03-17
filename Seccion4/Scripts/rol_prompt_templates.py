# El propósito de este script es demostrar cómo usar `ChatPromptTemplate` junto con `SystemMessagePromptTemplate` y `HumanMessagePromptTemplate` 
# para crear una plantilla de conversación estructurada. En este ejemplo, se define un rol para la IA, su especialidad, el tono de respuesta, 
# el tema de la pregunta y la pregunta misma. Luego, se formatea la plantilla con estos valores y se imprime el resultado.
# Esto ilustra que se puede generalizar el formato de mensajes para diferentes roles, especialidades, tonos y temas simplemente cambiando 
# los valores al formatear la plantilla.


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate 
from langchain_core.prompts import HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_humano
])

mensajes = chat_prompt.format_messages(
    rol="nutricionista",
    especialidad="dietas veganas",
    tono="profesional pero accesible",
    tema="proteínas vegetales",
    pregunta="¿Cuáles son las mejores fuentes de proteína vegana para un atleta profesional?"
)

for m in mensajes:
    print(m.content)