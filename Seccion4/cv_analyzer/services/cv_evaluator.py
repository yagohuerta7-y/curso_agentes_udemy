import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models.cv_models import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts

def crear_evaluador_cv():

    # Cargamos las variables de entorno
    load_dotenv()

    # Asignamos la api key a la variable de entorno
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    modelo_base = ChatOpenAI(
        model='gpt-5-nano-2025-08-07',
        temperature=0.0,
        api_key=OPENAI_API_KEY
    )

    # Con esto, las respuestas del LLM van a salir con la estructura del modelo de pydantic
    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)

    chat_prompt = crear_sistema_prompts()

    # Hacemos la cadena de avaluacion
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion


def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke(
            {
                'texto_cv': texto_cv,
                'descripcion_puesto': descripcion_puesto
            }
        )

        return resultado
    
    except Exception as e:
        return AnalisisCV(
            nombre_candidato='Error en el procesamiento',
            experiencia_anios=0,
            habilidades_clave=['Error al procesar el CV'],
            education='No se puede determinar',
            experiencia_relevante='Error durante el analisis',
            fortalezas=['Requiere revision manual del CV'],
            areas_mejora=['Verificar formato y legibilidad del PDF'],
            porcentaje_ajuste=0
        )
    
