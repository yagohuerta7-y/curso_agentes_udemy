# Para no saturar el context window de los modelos
# una tecnica que vamos a usar, es dividir el corpus 
# original del texto en pedazos mas pequenios, y eso se lo vamos a pasar al modelo

from pathlib import Path
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # Hace el chunking de manera inteligente


# --- Carga del pdf ---

# Definimos la ruta base
base_dir = Path(__file__).resolve().parent

# Armamos la ruta del archivo
file_path = base_dir / 'Data' / 'Contratos' / 'CONTRATO DE ARRENDAMIENTO DE LOCAL DE NEGOCIO 2.pdf'

# Cargamos el documento
loader = PyMuPDF4LLMLoader(file_path=file_path)
pages = loader.load()


# --- Hacemos el chunking del texto ---

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

chunks = text_splitter.split_documents(pages)


for i, chunk in enumerate(chunks):
    print(f'=== Chunk numero {i+1} ===')
    print(f'{chunk.page_content} \n')
