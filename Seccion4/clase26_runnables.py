# Los Runnables son cualquier objeto dentro de langchain que puedan invocarse.
# Osea, que se pueda usar el método .invoke()

from langchain_core.runnables import RunnableLambda

# Definimos una función básica
paso1 = RunnableLambda(lambda x: f"Numero {x} ")

# Definimos la otra función:
def duplicar_texto(texto: str):
    return [texto] * 2

paso2 = RunnableLambda(duplicar_texto)


# Hacemos la cadena
chain = paso1 | paso2


# Invocamos
resultado = chain.invoke(7)


print(resultado)