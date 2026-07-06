# Este script usa langchain community, la cual ya no va a tener soporte futuro.
# Entonces, este en un futuro puede que ya no sirva


import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader


# --- Configuracion del modelo y credenciales ---
  
# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definimos el modelo
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)


# --- Definimos las rutas de trabajo ---

# Definimos la ruta base (es decir, en donde esta el script)
base_dir = Path(__file__).resolve().parent

# Ruta del archivo pdf
files_path = base_dir / 'Data' / 'CV_Yago_Harvard_esp.pdf'


# --- Carga de documentos ---

# Cargamos mi cv
loader = PyPDFLoader(file_path=files_path)
docs = loader.load()


# --- Imprimimos el pdf ---

for i, page in enumerate(docs):
    print(f'=== Pagina {i+1} ===')
    print(f'Contenido: \n {page.page_content}')
    print(f'Metadatos: \n {page.metadata}')

