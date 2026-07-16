# ===== Clase para la creacion, insercion, y borrado de informacion a la Vector Data Base =====

# Importacion de credenciales y modelos
from services.credencials import Configuration
from config import DATA_DIR
from config import VDB_DIR

# Interaccion con el Sistema Operativo, y manejo de rutas
import logging
from pathlib import Path

# Base de datos vectorial
import chromadb
from langchain_chroma import Chroma
from chromadb.api.shared_system_client import SharedSystemClient

# Interaccion con modelos de OpenAI
from langchain_openai import OpenAIEmbeddings

# Para interactuar con los archivos que suba el usuario
from langchain_core.documents.base import Blob
from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class VDB:

    def __init__(self):
        '''
        Constructor donde definimos la ruta de donde se van a leer los archivos
        (los que sube el usuario) y el modelo de embeddings de OpenAI
        '''
        self.files_path = DATA_DIR
        self.embedding = Configuration().embedding_model

        self.docs = []
        self.docs_split = []
        self.vs = None
        self.vdb = None


    def carga_docs(self):
        '''
        Metodo para la carga de archivos del usuario
        '''
        self.docs = []
        parser = PyMuPDF4LLMParser()

        pdf_files = list(self.files_path.glob("*.pdf"))
        if not pdf_files:
            logger.warning("No se encontraron archivos PDF en %s", self.files_path)
            return self.docs

        for pdf_path in pdf_files:
            try:
                blob = Blob.from_path(pdf_path)
                self.docs.extend(parser.parse(blob))

            except Exception as e:
                logger.error("Error al procesar %s: %s", pdf_path.name, e)

        logger.info("Se cargaron %d documentos", len(self.docs))
        return self.docs
    

    def chunking(self):
        '''
        Metodo que define la forma de hacer los chunks de texto
        '''
        if not self.docs:
            logger.warning("No hay documentos cargados para hacer chunking")
            self.docs_split = []
            return self.docs_split

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        self.docs_split = text_splitter.split_documents(documents=self.docs)
        logger.info("Se generaron %d chunks", len(self.docs_split))
        return self.docs_split
    

    def creation(self):
        '''
        Metodo para la indexacion de los documentos a la base de datos
        '''
        if not self.docs_split:
            logger.warning("No hay chunks disponibles, no se creara la coleccion")
            return None

        try:
            SharedSystemClient.clear_system_cache()
            self.vs = Chroma.from_documents(
                documents=self.docs_split,
                embedding=self.embedding,
                persist_directory=str(VDB_DIR),
                collection_name="langchain"
            )
            logger.info("Coleccion creada correctamente")

        except Exception as e:
            logger.error("Error al crear la coleccion en Chroma: %s", e)
            self.vs = None

        return self.vs


    def delete(self):
        '''
        Método para eliminar todos los documentos de la VDB.
        Borra la colección y limpia los archivos del directorio VDB_DIR.
        '''
        client = None
        collection_name = getattr(self.vs, '_collection', None)
        collection_name = getattr(collection_name, 'name', 'langchain') if collection_name else 'langchain'

        try:
            client = chromadb.PersistentClient(path=str(VDB_DIR))
            try:
                client.delete_collection(collection_name)
                print(f"Colección '{collection_name}' eliminada correctamente.")
            except ValueError:
                print("La colección ya no existe o fue eliminada previamente.")
            except Exception as e:
                print(f"Error inesperado al eliminar la colección: {e}")

        except Exception as e:
            print(f"Error al conectar con Chroma para borrar: {e}")

        finally:
            SharedSystemClient.clear_system_cache()
            self.vs = None

            if VDB_DIR.exists():
                for ruta in VDB_DIR.iterdir():
                    if ruta.is_file():
                        try:
                            ruta.unlink()
                        except OSError as e:
                            print(f"No se pudo borrar {ruta.name}: {e}")


    def get_vs(self):
        '''
        Retorna la instancia de Chroma para hacer queries sobre la
        informacion existente. Si no esta cargada en memoria, la
        recupera desde el directorio persistido en disco.
        '''
        if self.vs is not None:
            return self.vs

        persist_dir = VDB_DIR

        if not persist_dir.exists():
            logger.warning("No existe una VDB persistida en %s", persist_dir)
            return None

        try:
            self.vs = Chroma(
                persist_directory=str(persist_dir),
                embedding_function=self.embedding
            )
            logger.info("Coleccion cargada desde %s", persist_dir)
        except Exception as e:
            logger.error("Error al cargar la coleccion existente: %s", e)
            self.vs = None

        return self.vs