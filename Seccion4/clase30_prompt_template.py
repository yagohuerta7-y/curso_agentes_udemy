# Recordemos que el PromptTemplate genera un string simple sin roles. No distingue entre system, user o assistant — solo rellena variables en un texto.
# Al diseñar plantillas, lo correcto es ponerlas en un script aparte, y hacerlas de una forma más modular.
# Aquí, vamos a aprender a ver cómo se ven nuestras plantillas al meterles texto dinámico sin tener la necesidad de pasarsela al LLM

from langchain_core.prompts import PromptTemplate

# En lugar de poner el template como texto crudo dentro de la clase, mejor lo separamos, para mayor orden
template = "Eres un experto en marketing. Sugiere un eslogan creativo para este producto: {producto}"

prompt = PromptTemplate(
    template=template,
    input_variables=["producto"]
)

# Aquí, introducimos las variables, para ver que es lo que va a recibir el LLM
prompt_lleno = prompt.format(producto = "Café orgánico")

print(prompt_lleno)