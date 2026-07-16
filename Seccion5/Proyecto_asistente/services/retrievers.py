# Importacion de credenciales y modelos
from services.credencials import Configuration

# Importacion de la VDB
from services.vdb import VDB

# Interaccion con el Sistema Operativo, y manejo de rutas
import logging
from pathlib import Path

# Base de datos vectorial
from langchain_chroma import Chroma

# Interaccion con modelos de OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# Para interactuar con los archivos que suba el usuario
from langchain_core.documents.base import Blob
from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Para hacer Querys a la DB
from langchain_classic.retrievers.multi_query import MultiQueryRetriever



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



class Retrievers:
    def __init__(self, query):

        vdb = VDB()
        vector_store = vdb.get_vs()

        if vector_store is None:
            raise RuntimeError("No se encontro una VDB persistida para crear el retriever")

        self.base_retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':5})
        
        self.retriever = MultiQueryRetriever.from_llm(
            retriever=self.base_retriever,
            llm=Configuration().llm_model
        )

        self.query = query


    def Query(self):
        try:
            self.resultado = self.retriever.invoke(self.query)
            return self.resultado

        except Exception as e:
            logger.error("Error al ejecutar la consulta: %s", e)
            return []