# Los Multi Query Retrivers es una clase de retrivers que usando LLM's reformulan una consulta en
# varias variantes (osea, consultas similares), para poder lanzar varias consultas en el vector store.
# Luego, fusiona los resultados de cada consulta, y elimina los duplicados.


import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever




# --- Cargamos las credenciales para el uso de modelos de OpenAI ---

# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el modelo de embeddings que vamos a usar
modelo_embeddings = OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=OPENAI_API_KEY
)

# Definimos el modelo de LLM que vamos a usar
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)



# --- Definimos la ruta de trabajo y de los archivos con los que vamos a trabajar ---

work_path = Path(__file__).resolve().parent



# --- Base de datos vectorial ---

# Como ya no la estamos creando, si no mas bien, usando, cambiamos los metodos que usamos
vectorstore = Chroma(
    embedding_function=modelo_embeddings,
    persist_directory=work_path/'Data'/'chroma_db'
)

# Definimos el retriver base
base_retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k':2})

# Ahora, definimos el MultiQueryRetriever
retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, 
    llm=llm
)

# Hacemos una consulta
query = 'Cual es el inmueble que forma parte del contrato en el que participa María Jiménez Campos?'
resultados = retriever.invoke(query)

print(f'Top 2 documentos mas similares a la consulta:\n\n')
for i, doc in enumerate(resultados, start=1):
    print(f'Contenido: \n {doc.page_content}')