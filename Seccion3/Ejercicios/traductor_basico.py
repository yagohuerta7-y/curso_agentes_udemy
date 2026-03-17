# Objetivo:   Crear un PromptTemplate que reciba tres variables: 
#                 - Un idioma de origen.
#                 - Un idioma de destino.
#                 - El texto a traducir.
    
# Instrucciones:  Usa la clase PromptTemplate. Asegúrate de que el template sea lo suficientemente robusto para que el LLM
#                 entienda que solo debe devolver la traducción, sin comentarios adicionales.
                
# Bonus:  Configura el template para que también acepte un "tono" (formal, informal, pirata, etc.).



# --- Importamos las dependencias ---

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate



# --- Configuraciones ---

# Cargamos las variables de entorno
load_dotenv()

# Guardamos la API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el LLM
llm = ChatOpenAI(
    model="gpt-5-nano-2025-08-07", 
    temperature=0.0, 
    api_key=OPENAI_API_KEY
    )



# --- Definimos la plantilla ---

plantilla = PromptTemplate(
    input_variables=["idioma_origen", "frase", "idioma_destino", "tono"],
    template="""
    Eres un traductor experto.
    Traduce del {idioma_origen} esta frase:
    {frase}
    A {idioma_destino} en un estilo {tono}
    
    Limitate a solo traducir, no respondas nada más.
    """
)



# --- Hacemos la cadena que ejecutará el agente ---

if __name__ == "__main__":

    chain = plantilla | llm

    resultado = chain.invoke(
        {
            "idioma_origen": "Español", 
            "frase": "Hola, te amo mi amor", 
            "idioma_destino": "Francés", 
            "tono": "Formal"
            }
        )

    print(f"Respuesta: \n{resultado.content}")