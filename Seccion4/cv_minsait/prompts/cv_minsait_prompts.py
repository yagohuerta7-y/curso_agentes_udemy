from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate 
from langchain_core.prompts import HumanMessagePromptTemplate


# Define el rol y criterios para el modelo de lenguaje
SYSTEM_INSTRUCTION  = SystemMessagePromptTemplate.from_template(
    '''
    Eres un reclutador senior con mas de 15 años de experiencia.
    Tu especialidad es analizar currículums y resumirlos con la información mas relevante.

    CRITERIOS:
    - Experiencia laboral relevante y progresión profesional
    - Habilidades técnicas y competencias específicas
    - Formación académica, certificaciones y educación continua
    '''
)

# Instrucciones especificas de que debe de hacer
ANALISIS_PROMPT = HumanMessagePromptTemplate.from_template(
    """Analiza el siguiente currículum y extrae la siguiente información:

**CURRÍCULUM VITAE DEL CANDIDATO:**
{texto_cv}

**INSTRUCCIONES ESPECÍFICAS:**
1. Nombre completo
2. Licenciatura
3. Maestria (si tiene)
4. Cursos
5. Habilidades duras
6. Herramientas que maneja el candidato
7. Idiomas que habla el candidato
8. Experiencia profesional
9. Trabajos en los que a estado, su fecha de inicio, fecha de salida y lo que a hecho (si tiene mucha experiencia, agarra los mas recientes)
"""
)

# Prompt combinado
CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        SYSTEM_INSTRUCTION,
        ANALISIS_PROMPT
    ]
)


def crear_sistema_prompts():
    """Crea el sistema de prompts especializado para análisis de CVs"""
    return CHAT_PROMPT