from pydantic import BaseModel
from pydantic import Field

class AnalisisCV(BaseModel):
    ''' 
    Modelo de datos para el analisis de un CV.
    '''
    nombre_candidato: str = Field(description='Nombre completo del candidato.')
    experiencia_anios: int = Field(description='Anios totales de experiencia laboral relevante.')
    habilidades_clave: list[str] = Field(description='Lista de las 5-7 habilidades del candidato mas relevante spara el puesto.')
    education: str = Field(description='Nivel educativo mas alto y especializacion principal.')
    experiencia_relevante: str = Field(description='Resumen conciso de la experiencia mas relevante para el puesto especifico.')
    fortalezas: list[str] = Field(description='3-5 principales fortalezas del candidato basadas en su perfil.')
    areas_mejora: list[str] = Field(description='2-4 areas donde el candidato podria desarrollarse y/o mejorar.')
    porcentaje_ajuste: int = Field(description='Porcentaje de ajuste al puesto (0-100) basado en experiencia, habilidades y formacion.', ge=0, le=100) # Aqui le decimos que el minimo debe de ser 0 y el maximo 100