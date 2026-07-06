import os
import tempfile
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

def extraer_texto(cv_candidato):
    '''
    Funcion que se encarga de extraer la informacion del cv del candidato (no funciona con imagenes)

    Args:
        cv_candidato: Archivo que va a subir el usuario

    Returns
        docs: Data del cv del candidato
    '''
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(cv_candidato.read())
            tmp_path = tmp.name

        loader = PyMuPDF4LLMLoader(tmp_path)
        docs = loader.load()
        texto = '\n'.join([page.page_content for page in docs])

        return texto

    except Exception as e:
        return f'Error al cargar el CV: \n {e}'

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)