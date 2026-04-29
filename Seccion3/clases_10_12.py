# Este script abarca los temas de las clases 10 a la 12, los cuales son:
# - Prompt template
# - Chains (la versión que tengo ya no tiene esto, me voy directo al siguiente tema)
# - LCEL (LangChain Expression Language)

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)


# Los Prompt templates son plantillas reutilizables para construir prompts dinámicos
# Vamos a hacer una plantilla, que retorne una respuesta de los 5 principales datos de algún personaje histórico
plantilla = PromptTemplate(
    input_variables = ["personaje"],
    template = """
    # Eres un historiador experto
    Vas a responder con los 5 datos que creas más relevantes de {personaje}
    """
)


# Las Chains son secuencias que encadenan los pasos anteriores
# La manera en que se deben de leer las cadenas es en este estilo:
chain = plantilla | llm # La plantilla se le proporciona al LLM

# Invocamos la cadena (ejecutamos)
resultado = chain.invoke({"personaje": "Albert Einstein"})
print(f"Respuesta: \n {resultado.content}")