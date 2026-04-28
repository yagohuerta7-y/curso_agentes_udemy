# Un Runnable es básicamente cualquier componente de LangChain que puede recibir una entrada, procesarla y devolver una salida. 
# Es la "interfaz común" que hace que todo en LangChain hable el mismo idioma.
# Otra forma de ver los Runnables es que son cualquier objeto dentro de langchain que puedan invocarse.
# Osea, que se pueda usar el método .invoke()

from langchain_core.runnables import RunnableLambda

# Definimos una función básica, que lo que hace es 
# recibir un número y devolver un string con ese número.
paso1 = RunnableLambda(lambda x: f"Numero {x}")

# Definimos la otra función, y esta lo que hace es 
# recibir un string y devolver una lista con ese string repetido dos veces.
def duplicar_texto(texto: str):
    return [texto] * 2

# Aquí, lo que hacemos es crear un Runnable a partir de la función que acabamos de definir.
paso2 = RunnableLambda(duplicar_texto)

# Hacemos la cadena, en la que el orden de lectura es de izquierda a derecha, osea, primero se ejecuta el paso1 y luego el paso2.
chain = paso1 | paso2

# Invocamos
resultado = chain.invoke(26)


print(resultado)