# En esta tarea, el objetivo es hacer un código de análisis de sentimientos.

# La estructura: 
# Texto de entrada → Preprocesamiento → Análisis Completo → Resultado
#                                            ↙        ↘
#                                     Resumen    Sentimiento

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


# --- Paso 0: Carga de credenciales y configuraciones ---

def carga_credenciales():
    """
    Función para cargar las credenciales del .env
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = carga_credenciales()

llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature = 0.0,
    api_key = OPENAI_API_KEY
)



# --- Paso 1: Preprocesamiento ---

def preprocess_text(text: str):
    """
    Función para limpiar el texto:
        Quitamos los espacios extras
        Limitamos la longitud a 500 caracteres

    Args:
        text (str): Mensaje del usuario
        
    Return:
        text (str): Texto tratado
    """
    
    # Quitamos los espacios extras
    text = text.strip()
    
    # Limitamos la longitud
    text = text[:500]
    
    return text


# Convertimos la función a un Runnable
preprocessor = RunnableLambda(preprocess_text)



# --- Paso 2: Análisis completo ---

# 2.1 Resumen
def generate_summary(text: str):
    """
    Función para generar un resumen del texto.
    
    Args:
        text (str): Texto tratado
        
    Return:
        summary (str): Resumen del texto
    """
    
    prompt = PromptTemplate(
        input_variables = ["text"],
        template = """
        # Eres un asistente que genera un resumen de un texto.
        
        Del siguiente texto, resumelo en una sola oración:\n
        {text}
        """
    )
    
    # Hacemos la cadena
    chain_resumen = prompt | llm
    
    # Invocamos la respuesta
    summary = chain_resumen.invoke({"text": text})
    
    return summary.content


# Convertimos la función a un Runnable
resumen = RunnableLambda(generate_summary)


# 2.2 Análisis de sentimientos
def analyze_sentiment(text: str):
    """
    Función para dictaminar el sentimiento de un texto

    Args:
        text (str): resumen del texto
        
    Return:
        sentiment (str): Sentimiento del texto
    """
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        # Rol: Eres un experto de extraordinaria sensibilidad, capaz de dictaminar el sentimiento de un texto con gran precisión.
    
        Analiza el sentimiento del siguiente texto, y clasificalo en alguna de las siguientes tres categorías:
        - Positivo
        - Negativo
        - Neutro
        
        Texto:\n
        {text}
        
        Responde de manera estructurada con un JSON válido:
        {{
            'sentimiento': 'positivo', 'negativo', 'neutro',
            'razon': 'justificación breve de tu respuesta'
        }}
        """
    )
    
    chain_sentimiento = prompt | llm
        
    sentimientos = chain_sentimiento.invoke({"text": text})
    
    try:
        return json.loads(sentimientos.content)
    
    except json.JSONDecodeError:
        return {
            'sentimiento': 'desconocido',
            'razon': 'No se pudo determinar el sentimiento debido a un error en la respuesta del modelo.'
        }
    

# Convertimos la función a un Runnable
analisis_sentimientos = RunnableLambda(analyze_sentiment)



# --- Paso 3: Resultado ---

# Combinamos los resultados del resumen, y el análisis de sentimientos
def merge_results(resumen: str, sentimientos: json.JSONEncoder):
    """
    Función para combinar los resultados del resumen y el análisis de sentimientos.

    Args:
        resumen (str): _description_
        sentimientos (dict): JSON con el sentimiento del texto
    """
    
    return {
        "resumen": resumen,
        "sentimiento": sentimientos["sentimiento"],
        "razon": sentimientos["razon"] 
    }
    
    
# Gestionamos la cadena de procesamiento
def pipeline_procesamiento(text: str):
    """
    Esta función es para coordinar los pasos

    Args:
        text (str): Texto a analizar
    """
    
    resumen_del_texto = resumen.invoke(text)
    sentimientos_del_texto = analisis_sentimientos.invoke(text)
    
    return merge_results(
        resumen = resumen_del_texto, 
        sentimientos = sentimientos_del_texto
        )
    
process = RunnableLambda(pipeline_procesamiento)



def main():
    
    # Conectamos todo el flujo
    chain = preprocessor | process
    
    textos_prueba = [
        "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
        "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
        "El clima está nublado hoy, probablemente llueva más tarde.",
        "Te quiero muchísimo, pero no puedo seguir con esto"
    ]
    
    for texto in textos_prueba:
        print(f"El texto a analizar es:\n {texto}")
        resultado = chain.invoke(texto)
        print(f"\n Resultado:\n {resultado}")
        print("-" * 50)
        


if __name__ == "__main__":
    main()
