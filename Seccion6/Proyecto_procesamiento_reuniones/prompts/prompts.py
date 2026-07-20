from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate 
from langchain_core.prompts import HumanMessagePromptTemplate


class Prompts:
    '''
    Clase para almacenar todos los prompts
    '''
    def __init__(self):
        self.rol = SystemMessagePromptTemplate.from_template(
            template='''
            Eres un asistente ejecutivo con mucha experiencia, tu labor es, dada transcripciones de reuniones, responder lo que se te pida
            '''
        )


    def prompt_lista_participantes(self):
        self.participante = HumanMessagePromptTemplate.from_template(
            template='''
            Dado el siguiente texto, extrae la lista de participantes: {texto}
            '''
        )

        self.chat_prompt_participantes = ChatPromptTemplate.from_messages([
            self.rol,
            self.participante
        ])

        return self.chat_prompt_participantes


    def prompt_acciones(self):
        self.acciones = HumanMessagePromptTemplate.from_template(
            template='''
            Dados los siguientes participantes, y el siguiente texto, extrae las acciones acordadas con responsables asignados:
            \nParticipantes:\n{participantes}
            \nTexto:\n{texto}
            '''
        )

        self.chat_prompt_acciones = ChatPromptTemplate.from_messages([
            self.rol,
            self.acciones
        ])

        return self.chat_prompt_acciones


    def prompt_temas_principales(self):
        self.principales = HumanMessagePromptTemplate.from_template(
            template='''
            Dado el siguiente texto, extrae los temas principales discutidos: {texto}
            '''
        )

        self.chat_prompt_principales = ChatPromptTemplate.from_messages([
            self.rol,
            self.principales
        ])

        return self.chat_prompt_principales


    def prompt_resumen(self):
        self.resumen = HumanMessagePromptTemplate.from_template(
            template='''
            Dado el siguiente texto, elabora un resumen ejecutivo conciso de la reunion (máximo 30 palabras): {texto}
            '''
        )

        self.chat_prompt_resumen = ChatPromptTemplate.from_messages([
            self.rol,
            self.resumen
        ])

        return self.chat_prompt_resumen


    def prompt_minuta(self):
        self.minuta = HumanMessagePromptTemplate.from_template(
            template='''
            Dados los participantes, y las acciones, construye la minuta (máximo 150 palabras):
            \nParticipantes: {participantes}\n\nAcciones:\n{acciones}
            '''
        )

        self.chat_prompt_minuta = ChatPromptTemplate.from_messages([
            self.rol,
            self.minuta
        ])

        return self.chat_prompt_minuta