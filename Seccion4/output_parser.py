# Este script une todos los conceptos que hemos visto en esta sección para crear un análisis de texto con salida estructurada. 
# Para esto, vamos a usar Pydantic para definir la estructura de la salida que queremos del modelo, y luego vamos a usar esa estructura 
# para obtener una respuesta más precisa y fácil de manejar.
#     - Usaremos: pydantic para la validación y estructura de los datos.
#     - Usaremos: `with_structured_output` para obtener una respuesta formateada.
#     - Usaremos: platillas de prompts para separar las instrucciones del sistema y los mensajes del humano, 
#                 lo que nos permitirá tener una conversación más fluida y estructurada con el modelo.

# Para cargar las variables de entorno
import os
from dotenv import load_dotenv

# Para la verificación de datos
from pydantic import BaseModel
from pydantic import Field

# Para poder interactuar con los modelos de OpenAI
from langchain_openai import ChatOpenAI

# Para manejar los mensajes de la conversación (no se usan aquí)
# from langchain_core.messages import HumanMessage
# from langchain_core.messages import AIMessage

# Para definir la plantilla de mensajes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate


# Cargamos las credenciales
def get_credenciales():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")
    
OPENAI_API_KEY = get_credenciales()


# Creamos la clase para el análisis de texto, con Pydantic para validar los datos que recibimos del modelo
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen del texto")
    sentimiento: str = Field(description="Sentimiento del texto (Positivo, Negativo, Neutro)")
    razon: str = Field(description="Razón del sentimiento")


# Hacemos el system instruction
instrucciones_del_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} extremadamente preciso en {actividad}."
)

# Hacemos la plantilla para el mensaje del humano
plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Quiero que realices esta tarea: {tarea} con este texto: {texto}"
)

# Hacemos la platilla de la conversación con ambas plantillas (la del sistema y la del humano)
plantilla_chat = ChatPromptTemplate.from_messages(
    [
        instrucciones_del_sistema,
        plantilla_humano
    ]
)

# Los mensajes que queremos enviar al modelo, con los valores para cada variable de las plantillas lo podemos formatear la plantilla de la conversación
mensajes = plantilla_chat.format_messages(
    rol = "Analizador de textos",
    actividad = "Clasificar sentimientos",
    tarea = "Retorna una clasificación del sentimiento del texto (Positivo, Negativo, Neutro) y un resumen del mismo",
    texto = "Me encantó tu postre mami, es riquísimo"
)



# Instanciamos el modelo de llm que queremos
llm = ChatOpenAI(
    model = "gpt-5-nano-2025-08-07",
    temperature = 0.0,
    api_key = OPENAI_API_KEY
)


# Hacemos una nueva instancia del LLM pero que saque la respuesta estructurada
llm_structurado = llm.with_structured_output(AnalisisTexto) # Aquí le decimos que queremos que la salida del modelo sea de tipo AnalisisTexto, que es la clase que hemos creado con Pydantic.

# Ahora sí, hacemos la consulta al modelo con los mensajes que hemos formateado y obtenemos el resultado estructurado
resultado = llm_structurado.invoke(mensajes)

# print(resultado) # Este te imprime algo distinto
print(resultado.model_dump_json(indent=2)) # Forzamos que retorne un JSON