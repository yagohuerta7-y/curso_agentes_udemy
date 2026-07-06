from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from typing import List


class Trabajo(BaseModel):
    '''
    Modelo de un trabajo dentro de la experiencia profesional del candidato
    '''

    puesto: str = Field(description='Nombre del puesto o cargo')
    empresa: str = Field(description='Empresa donde trabajo el candidato')
    fecha_inicio: str = Field(description='Fecha de inicio del trabajo')
    fecha_fin: Optional[str] = Field(
        default=None,
        description='Fecha de fin del trabajo, o None si es el actual'
    )
    actividades: List[str] = Field(
        min_length=3,
        max_length=3,
        description='Exactamente 3 actividades principales realizadas en el puesto'
    )


class DataCV(BaseModel):
    '''
    Modelo de datos para el proyecto de CV Minsait
    '''

    nombre: str = Field(description='Nombre completo del candidato')
    licenciatura: str = Field(description='Licenciatura del candidato (y su universidad)')
    maestria: Optional[str] = Field(
        default=None,
        description='Maestria del candidato (y su universidad)'
        )
    cursos: List[str] = Field(
        min_length=1,
        max_length=4,
        description='1-4 cursos mas relevantes del candidato (si tiene)'
        )
    hab_duras: str = Field(description='Keywords de las habilidades del candidato (ej. Agentes, ML & AI, etc)')
    herramientas: str = Field(description='Keywords de las tecnologias que maneja el candidato (ej. Excel, MySQL, Python, etc)')
    idiomas: str = Field(description='Idiomas que habla el candidato, y de ser posible su nivel')
    exp_prof: str = Field(description='Resumen de 50-150 palabras de la experiencia del candidato')
    trabajos: List[Trabajo] = Field(
        min_length=1,
        max_length=3,
        description='Entre 1 y 3 trabajos mas relevantes del candidato'
    )