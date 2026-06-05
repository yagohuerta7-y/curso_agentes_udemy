# Vamos a hacer un programa que haga análisis de sentimientos con un LLM
# La arquitectura del sistema es esta:
#     Texto de entrada → Preprocesamiento → Análisis Completo → Resultado
#                                               ↙        ↘
#                                              Resumen    Sentimiento

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuramos el mondelo de lenguaje que vamos a usar 
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)



def preprocess_text(texto: str)-> str:
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



def generate_resumen(texto: str):
    """ 
    Esta función es la encargada de generar el resumen del texto
    
    Args:
        text (str): Texto al que le vamos a aplicar un resumen
    """
    # Definimos el template para el comportamiento del generador de resumenes
    promptResumen = PromptTemplate(
        input_variables=["texto"],
        template="""
        Eres un asistente el cual tu única tarea es resumir el siguiente texto: 
        {texto} 
        """
    )
    
    chain = promptResumen | llm
    respuesta = chain.invoke({"texto": texto})
    
    return respuesta.content

# Lo transformamos en un Runnable
resumen = RunnableLambda(generate_resumen)



def analyze_sentiment(texto: str) -> dict:
    """ 
    Esta función es la encargada de hacer el análisis de sentimiento del texto
    
    Args:
        text (str): Texto al que le vamos a hacer el análisis de sentimiento

    Returns:
        dict: Un diccionario con el sentimiento (positivo, negativo o neutro) y una breve justificación del por qué se clasificó de esa manera
    """
    # Definimos el template para el comportamiento del modelo al clasificar los sentimientos
    promptSentimiento = PromptTemplate(
        input_variables=["texto"],
        template="""
        Eres un analizador de sentimientos experto. Tu tarea es dado un texto que se te va a proporcionar, respondas únicamente en este formato JSON:
        {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
        
        El texto el el siguiente:
        {texto}
        """
    )

    chain = promptSentimiento | llm
    respuesta = chain.invoke({"texto": texto})
    
    try:
        return json.loads(respuesta.content)
    
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

# Lo transformamos en un Runnable
analisis = RunnableLambda(analyze_sentiment)




def main():
    
    text = "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido."
    
    paso1 = preprocessor | resumen
    paso2 = preprocessor | analisis
    
    datos = {
        "resumen": paso1.invoke(text),
        "sentimiento" : paso2.invoke(text)['sentimiento'],
        "razon": paso2.invoke(text)['razon']
    }
    
    print(datos)
    
    return datos

if __name__ == "__main__":
    main()