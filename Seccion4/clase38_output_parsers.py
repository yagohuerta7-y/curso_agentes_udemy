# El propósito de este script, es replicar el análisis de sentimientos que teníamos, pero ahora estructurando la respuesta del modelo usando pydantic.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from pydantic import Field
from pydantic import BaseModel


# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)


# Hacemos la clase de nuestro modelo de datos
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento del texto (Positivo, Negativo o Neutro)")


# Transformamos la salida del LLM en un objeto estructurado (el modelo de LLM debe de soportar salida estructurada)
structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encantó la nueva película de acción, tiene muchos efectos especiales y te provoca muchas emociones muy diversas"

resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_prueba}")

# print(resultado) # Esto imprime: resumen='La persona disfrutó de la nueva película de acción, destacando sus efectos especiales y las emociones variadas que le provocó.' sentimiento='Positivo'

print(resultado.model_dump_json()) # Esto lo imprime como un Json


# NOTA: Faltaron varias cosas (procesamiento de batch, etc), pero solo era para ejemplificar las salidas estrucutradas con un ejemplo conocido.