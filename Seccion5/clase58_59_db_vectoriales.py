# Este es el primer paso en la construccion de RAG's

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma # A diferencia del video, aqui lo implemento de la forma moderna
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents.base import Blob
from langchain_pymupdf4llm import PyMuPDF4LLMParser # Una clase para poder subir archivos de una manera mas flexible
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
files_path = work_path / 'Data' / 'Contratos'



# --- Cargamos el directorio de los archivos a analizar ---

# Para no usar elementos de langchain_community (ya que va a ser deprecado), cargamos el directorio 
# de una manera mas entandar, recorriendo el directorio, y cargando cada documento

loader = PyMuPDF4LLMParser()
docs = []

for pdf_path in Path(files_path).glob("*.pdf"):  # recorre cada PDF en la carpeta
    blob = Blob.from_path(pdf_path)              # envuelve el archivo como Blob (lectura perezosa)
    docs.extend(loader.parse(blob))              # parsea el Blob y agrega sus Documents a la lista

print(f'Se cargaron {len(docs)} archivos desde el directorio {files_path}.')



# --- Hacemos los chunks ---

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs_split = text_splitter.split_documents(documents=docs)

print(f'Se crearon {len(docs_split)} chunks de texto.')



# --- Base de datos vectorial ---

# Creamos la base de datos vectorial usando los documentos a los que les hicimos chunks
vectorstore = Chroma.from_documents(
    documents=docs_split,
    embedding=modelo_embeddings,
    persist_directory=work_path/'Data'/'chroma_db'
)

# Hacemos una consulta
query = 'Cual es el inmueble que forma parte del contrato en el que participa María Jiménez Campos?'
resultados = vectorstore.similarity_search(
    query,
    k=2 # Nos da los 2 resultados mas relevantes
)

print(f'Top 2 documentos mas similares a la consulta:\n\n')
for i, doc in enumerate(resultados, start=1):
    print(f'Contenido: \n {doc.page_content}')