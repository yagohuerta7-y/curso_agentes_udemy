from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate


system_instruction = SystemMessagePromptTemplate.from_template('''
# Rol
Eres un asistente experto, tu mision es responderle al usuario **unicamente** con la informacion que tengas disponible.

# Tono
Breve, amable, directo
'''
)

prompt = HumanMessagePromptTemplate.from_template('''
Analiza la pregunta que te hace el usuario: \n{query}\n
Y con esta informacion, responde a su pregunta: \n{retrievers}
'''
)

chat_prompt = ChatPromptTemplate(
    [
        system_instruction,
        prompt
    ]
)


def crear_sistema_prompts():
    return chat_prompt