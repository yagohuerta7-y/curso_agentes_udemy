# Importamos las dependencias

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


# Cargamos la variable de entorno de la api key
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el modelo
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)

# Definimos la plantilla
plantilla = PromptTemplate(
    input_variables=["nombre"], # Valor que vamos a sustituir/insertar en el prompt
    template="""
    # Eres un escritor sumamente sensible y experto en crear poemas
    
    Escribe un poema con el nombre {nombre}\n
    """
)

# Hacemos la cadena
chain = plantilla | llm # La plantilla se le pasa al llm

# Invocamos la respuesta, y le pasamos la variable que necesita el template
resultado = chain.invoke({"nombre": "Yago"})

# Mostramos la respuesta
print(f"Respuesta: {resultado.content}")