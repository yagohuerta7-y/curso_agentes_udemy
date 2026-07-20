from openai import OpenAI
from services.credentials import Credentials

from prompts.prompts import Prompts

from models.flujo_models import Participante
from models.flujo_models import Participantes
from models.flujo_models import AccionPorParticipante
from models.flujo_models import Acciones
from models.flujo_models import Minuta
from models.flujo_models import Temas_principales

from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END



class State(TypedDict):
        file_path: str # Path del archivo .mp4
        texto_original: str
        participantes: list[Participante]
        temas_principales: Temas_principales
        acciones: list[AccionPorParticipante]
        minuta: Minuta
        resumen: str


class Transcribe:
    def __init__(self):
        self.credentials = Credentials().openai_api_key
        self.client = OpenAI(api_key=self.credentials)        

    def transcribe(self, state: State):

        with open(state['file_path'], 'rb') as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language='es'
            )
        
        return {'texto_original': transcript.text}


class Node_functions:
    def __init__(self):

        # --- Credenciales ---
        self.base_llm = Credentials().llm_model


        # --- Trios Prompt - LLM - Chain ---

        # Trio para obtener los participantes
        self.prompt_participantes = Prompts().prompt_lista_participantes()
        self.participantes_llm = self.base_llm.with_structured_output(Participantes)
        self.chain_participantes = self.prompt_participantes | self.participantes_llm

        # Trio para obtener las acciones asignadas
        self.prompt_acciones =  Prompts().prompt_acciones()
        self.acciones_llm = self.base_llm.with_structured_output(Acciones)
        self.chain_acciones = self.prompt_acciones | self.acciones_llm

        # Trio para obtener los temas principales
        self.prompt_temas =  Prompts().prompt_temas_principales()
        self.temas_llm = self.base_llm.with_structured_output(Temas_principales)
        self.chain_temas = self.prompt_temas | self.temas_llm

        # Trio para obtener la minuta
        self.prompt_minuta =  Prompts().prompt_minuta()
        self.minuta_llm = self.base_llm.with_structured_output(Minuta)
        self.chain_minuta = self.prompt_minuta | self.minuta_llm

        # Trio para obtener la resumen
        self.prompt_resumen =  Prompts().prompt_resumen()
        self.chain_resumen = self.prompt_resumen | self.base_llm # Este no tiene una clase de Pydatic



    def Get_participantes(self, state: State):
        '''
        Metodo del nodo para extraer los participantes de la transcripcion
        '''

        # Hacemos la invocacion
        self.participantes = self.chain_participantes.invoke({'texto': state['texto_original']})

        return {'participantes': self.participantes.participantes}
    
    
    def Get_acciones(self, state: State):
        '''
        Metodo del nodo para extraer las acciones por participantes
        '''

        # Hacemos la invocacion
        self.acciones = self.chain_acciones.invoke({'participantes': state['participantes'], 'texto': state['texto_original']})

        return {'acciones': self.acciones.acciones}


    def Get_temas(self, state: State):
        '''
        Metodo del nodo para extraer los temas principales de la reunion
        '''

        # Hacemos la invocacion
        self.temas = self.chain_temas.invoke({'texto': state['texto_original']})

        return {'temas_principales': self.temas}
    

    def Get_minuta(self, state: State):
        '''
        Metodo del nodo para extraer la minuta de la reunion
        '''

        # Hacemos la invocacion
        self.minuta = self.chain_minuta.invoke({'participantes': state['participantes'], 'acciones': state['acciones']})

        return {'minuta': self.minuta}
    

    def Get_resumen(self, state: State):
        '''
        Metodo del nodo para extraer el resumen de la reunion
        '''

        # Hacemos la invocacion
        self.resumen = self.chain_resumen.invoke({'texto': state['texto_original']})

        return {'resumen': self.resumen}