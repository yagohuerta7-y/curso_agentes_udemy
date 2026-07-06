# Este script incluye metodos mas modernos de los vistos en la clase 51, pero
# nos vamos a basar en esa clase para entender el contenido.
# Pruebo dos dependencias para hacer la extraccion de contenido de mi cv

from pathlib import Path
# from langchain_docling import DoclingLoader # Este usa modelos OCR, es muy bueno y sirve para diferentes tipos de documentos (pdf, docx, pptx, etc)
from langchain_pymupdf4llm import PyMuPDF4LLMLoader # Este funciona Tesseract, pero no necesita descargar los pesos de HF


# --- Definimos las rutas de trabajo ---

# Definimos la ruta base (es en donde esta el script)
base_dir = Path(__file__).resolve().parent

# Ruta del archivo PDF
file_path = base_dir / 'Data' / 'CV_Yago_Harvard_esp.pdf'


# --- Carga de documentos ---

# Con DoclingLoader
# loader = DoclingLoader(file_path=file_path)

# Con PyMuPDF4LLMLoader
loader = PyMuPDF4LLMLoader(file_path=file_path)
docs = loader.load()


# --- Visualizacion del contenido ---
for i, page in enumerate(docs):
    print(f'=== Pagina {i+1} ===')
    print(f'Contenido: \n {page.page_content}\n')
    # print(f'Metadatos: \n {page.metadata} \n\n')