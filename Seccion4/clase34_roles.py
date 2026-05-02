# Cuando se trabajan en proyectos grandes, lo conveniente es modularizar los componentes, eso incluye las plantillas.
# En este script vamos a ver cómo se definen los roles para un modelo.
# Como referencia para el futuro Yago, observa este diagrama:

        # GRUPO 1 — Herramientas para CONSTRUIR prompts (antes de invocar)
        # ├── ChatPromptTemplate
        # ├── SystemMessagePromptTemplate
        # └── HumanMessagePromptTemplate

        # GRUPO 2 — Objetos que REPRESENTAN mensajes (el resultado final)
        # ├── SystemMessage
        # ├── HumanMessage
        # └── AIMessage
        
# Para que no te hagas bolas por ver cosas similares, pues sus propósitos son distintos.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate



# Empezamos con la creación de las plantillas dinámicas

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}."
)

# Al usar el .from_template, es una forma más rápida en lugar de hacer:
# plantilla_sistema = SystemMessagePromptTemplate(
#     prompt=PromptTemplate(
#         input_variables=["rol", "especialidad", "tono"],
#         template="Eres un {rol} especializado en {especialidad}. Responde de manera {tono}."
#     )
# )

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

# Componemos las plantillas anteriores
chat_prompt = ChatPromptTemplate(
    [
        plantilla_sistema,
        plantilla_humano
    ]
)

# Veamos como se estructura
mensajes = chat_prompt.format_messages(
    rol = "Nutricionista",
    especialidad = "Dietas veganas",
    tono = "Profesional, pero muy amable",
    tema = "Proteínas vegetales",
    pregunta = "¿Cuales son las mejores opciones de proteína vegetal para sustituír la carne de nuestra dieta?"
)

for mensaje in mensajes:
    print(f"{mensaje.__class__.__name__}: {mensaje.content}")