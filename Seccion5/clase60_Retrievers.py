# Los retrivers se van a encargar que dada una query, busquen y retornen los documentos relevantes
# Es decir, encapsulan la logica de la busqueda.
# Un retriver es el componente fundamental de un RAG, y es mas general que una vector store, pues toda vector store
# puede ser un retriver, pero no todos los retrivers son vector stores, hay retrivers que van a buscar a internet, por ejemplo
# Vamos a usar lo que ya tenemos almacenada en Chroma.

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings



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



# --- Definimos la ruta de trabajo y de los archivos con los que vamos a trabajar ---

work_path = Path(__file__).resolve().parent




# --- Base de datos vectorial ---

# Como ya no la estamos creando, si no mas bien, usando, cambiamos los metodos que usamos
vectorstore = Chroma(
    embedding_function=modelo_embeddings,
    persist_directory=work_path/'Data'/'chroma_db'
)

# Definimos el retriver
retriver = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k':2})

# Hacemos una consulta
query = 'Cual es el inmueble que forma parte del contrato en el que participa María Jiménez Campos?'
resultados = retriver.invoke(query)

print(f'Top 2 documentos mas similares a la consulta:\n\n')
for i, doc in enumerate(resultados, start=1):
    print(f'Contenido: \n {doc.page_content}')