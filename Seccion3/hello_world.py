# Importamos las dependencias

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Cargamos la variable de entorno de la api key
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el modelo
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)

# Guardamos la pregunta en unna variable
pregunta = "Explícame las direncias entre la integral de Riemann y la de Lebesgue"

# Hacemos la inferencia
respuesta = llm.invoke(pregunta)

# Mostramos la respuesta
print(f"Respuesta: {respuesta}")