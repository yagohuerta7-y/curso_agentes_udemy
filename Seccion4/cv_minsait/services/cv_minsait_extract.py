import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models.cv_minsait_models import Trabajo
from models.cv_minsait_models import DataCV
from prompts.cv_minsait_prompts import crear_sistema_prompts
from services.load_data import extraer_texto

def crear_extractor_cv():
    '''
    Esta funcion crea el modelo con la salida estructurada. Y creamos la chain de procesamiento
    '''

    # Cargamos las variables de entorno
    load_dotenv()

    # Asignamos la api key a la variable de entorno
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Definimos el modelo de lenguaje que vamos a usar
    modelo_base = ChatOpenAI(
        model='gpt-5-nano-2025-08-07',
        temperature=0.0,
        api_key=OPENAI_API_KEY
    )

    # Hacemos que las respuestas del modelo de lenguaje sigan la estructura definida
    modelo_estructurado = modelo_base.with_structured_output(DataCV)

    # Creamos el prompt
    prompt = crear_sistema_prompts()


    # Definimos la chain
    chain_extractor = prompt | modelo_estructurado

    return chain_extractor


def extraer(CV):
    '''
    En esta funcion solo se va a encargar de llamar a la funcion de arriba, y procesar el cv
    '''
    # Extraemos el texto del CV
    texto_cv = extraer_texto(CV)

    chain = crear_extractor_cv()

    try:
        resultado = chain.invoke({'texto_cv': texto_cv})
        return resultado.model_dump()

    except Exception as e:
        return f'Error: \n {e}'





