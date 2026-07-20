from config import DATA_DIR

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from services.node_functions import State
from services.node_functions import Transcribe
from services.node_functions import Node_functions



def main():

    # 0. Definimos la ruta de nuestro audio
    audio = DATA_DIR / 'Simulacion_reunion.mp4'


    # 1. Traemos el esquema del estado (ya lo importe)
    
    # 2. Creamos el grafo de estado
    graph = StateGraph(State)

    # 3. Declaramos las funciones de los nodos
    transcripcion = Transcribe().transcribe
    participantes = Node_functions().Get_participantes
    acciones = Node_functions().Get_acciones
    temas_principales = Node_functions().Get_temas
    minuta = Node_functions().Get_minuta
    resumen = Node_functions().Get_resumen

    # 4. Agregamos los nodos al grafo
    graph.add_node('Transcribe', transcripcion)
    graph.add_node('Get_participantes', participantes)
    graph.add_node('Get_acciones', acciones)
    graph.add_node('Get_temas', temas_principales)
    graph.add_node('Get_minuta', minuta)
    graph.add_node('Get_resumen', resumen)

    # 5. Conectamos los nodos en secuancia
    graph.add_edge(START, 'Transcribe')
    graph.add_edge('Transcribe', 'Get_participantes')
    graph.add_edge('Get_participantes', 'Get_acciones')
    graph.add_edge('Get_acciones', 'Get_temas')
    graph.add_edge('Get_acciones', 'Get_minuta')
    graph.add_edge('Get_acciones', 'Get_resumen')
    graph.add_edge('Get_temas', END)
    graph.add_edge('Get_minuta', END)
    graph.add_edge('Get_resumen', END)

    # 6. Compilar el grafo
    compiled_graph = graph.compile()

    # 7. Invocamos el grafo
    resultado = compiled_graph.invoke({'file_path': audio})

    print(resultado)



if __name__ == "__main__":
    main()