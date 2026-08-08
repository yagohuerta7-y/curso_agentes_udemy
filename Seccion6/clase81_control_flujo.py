from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Definimos el estado
class State(TypedDict):
    numero: int
    resultado: str

# Creamos el grafo
graph = StateGraph(State)


# Definimos los nodos del workflow
def caso_par(state):
    return {'resultado': f'El numero {state["numero"]} es par'}

def caso_impar(state):
    return {'resultado': f'El numero {state["numero"]} impar'}


# Agregamos los nodos al grafo
graph.add_node('Par', caso_par)
graph.add_node('Impar', caso_impar)


# Definimos la funcion de routing para decidir la rama de ejecucion
def decidir_rama(state):
    if state['numero'] %2 == 0:
        return 'Par'

    else:
        return 'Impar'


# Agregamos el edge condicional al flujo
graph.add_conditional_edges(START, decidir_rama, {'Par': 'Par', 'Impar': 'Impar'}) # En lo ultimo hacemos el mapeo a los nodos destino


# Conectar ambos casos al final
graph.add_edge('Par', END)
graph.add_edge('Impar', END)

compile = graph.compile()


# Probamos el grafo con ejemplos

print(compile.invoke({"numero": 4}))