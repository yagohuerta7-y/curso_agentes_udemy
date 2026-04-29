# En esta clase, vamos a seguir con el proyecto de clasificación de sentimientos, pero introsuciendo el concepto de RunnableParallel.
# Es un Runnable que ejecuta múltiples Runnables al mismo tiempo con la misma entrada, y agrupa todos sus resultados en un solo diccionario.
    
#            input
#              │
#     ┌────────┼────────┐
#     │        │        │
# runnable_A  runnable_B  runnable_C
#     │        │        │
#  salida_A  salida_B  salida_C
#     │        │        │
#     └────────┼────────┘
#              │
#     {
#       "clave_A": salida_A,
#       "clave_B": salida_B,
#       "clave_C": salida_C
#     }
    
# Vamos a tomar el código de la clase pasada, y lo vamos a mejorar, agregando en dónde es debido esta nueva funcionalidad
# Y esto es, en el resumen, y en la clasificación del sentimiento.

import os
import json
from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableParallel


# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)


# Definimos el template para el comportamiento del generador de resumenes
prompt_resumen = PromptTemplate(
    input_variables=["texto"],
    template="""
        Eres un asistente el cual tu única tarea es resumir el siguiente texto: 
        {texto} 
    """
)

# Definimos el template para el comportamiento del modelo al clasificar los sentimientos
prompt_sentimiento = PromptTemplate(
    input_variables=["texto"],
    template="""
        Eres un analizador de sentimientos experto. Tu tarea es dado un texto que se te va a proporcionar, respondas únicamente en este formato JSON:
        {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
            
        El texto el el siguiente:
        {texto}
    """
    )




def preprocess_text(texto: str):
    """ 
    Función que limpia el texto de entrada (eliminando espacios extras y limitando la longitud a 500 caracteres)
    
    Args:
        text (str): Cadena de entrada
        
    Returns:
        str
    """
    texto = texto[:500]
    return texto.strip()

# Lo transformamos en un Runnable
preprocessor = RunnableLambda(preprocess_text)



def generate_resumen(texto: str) -> str:
    """ 
    Esta función es la encargada de generar el resumen del texto
    
    Args:
        text (str): Texto al que le vamos a aplicar un resumen
    """
    chain = prompt_resumen | llm
    respuesta = chain.invoke({"texto": texto})
    
    return respuesta.content

# Lo transformamos en un Runnable
resumen_branch = RunnableLambda(generate_resumen)



def analyze_sentiment(texto: str) -> dict[str, str]:
    """ 
    Esta función es la encargada de hacer el análisis de sentimiento del texto
    
    Args:
        text (str): Texto al que le vamos a hacer el análisis de sentimiento
        
    Returns:
        dict: Diccionario que sigue la siguiente estructura:
        {
            'sentimiento': str, 
            'razon': str
        }
    """
    chain = prompt_sentimiento | llm
    respuesta = chain.invoke({"texto": texto})
    
    try:
        return json.loads(respuesta.content)
    
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

# Lo transformamos en un Runnable
analisis_branch = RunnableLambda(analyze_sentiment)



def merge(data: dict[str, Any]) -> dict[str, str]:
    """Función que en un solo JSON junta la información de los distintos procesos 

    Args:
        data (dict): Diccionario con los datos que nos interesa.

    Returns:
        dict: Diccionario que sigue la siguiente estructura:
        {
            'resumen': str, 
            'sentimiento': str, 
            'razon': str
        }
    """
    
    return {
        "resumen": data['resumen'],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }
    
# Lo transformamos en un Runnable
unir = RunnableLambda(merge)



def main():
    
    text = "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido."
    
    parallel = RunnableParallel(
        {
            "resumen": resumen_branch,
            "sentimiento_data": analisis_branch
        }
    )
    
    chain = preprocessor | parallel | unir
    
    
    resultado = chain.invoke(text)
    
    print(resultado)
    
    return resultado

if __name__ == "__main__":
    main()