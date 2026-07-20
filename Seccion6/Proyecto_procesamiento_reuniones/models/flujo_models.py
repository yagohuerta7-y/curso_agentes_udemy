from pydantic import BaseModel, Field


class Participante(BaseModel):
    nombre: str = Field(
        min_length=1,
        description="Nombre del participante.",
    )


class Actividad(BaseModel):
    actividad: str = Field(
        min_length=1,
        description="Actividad o tarea mencionada en la reunión.",
    )


class AccionPorParticipante(BaseModel):
    participante: Participante = Field(
        description="Participante al que se le asignan las actividades.",
    )
    actividades: list[Actividad] = Field(
        min_length=1,
        description="Actividades asignadas al participante.",
    )


class Minuta(BaseModel):
    participantes: list[Participante] = Field(
        min_length=1,
        description="Participantes presentes o mencionados.",
    )
    acciones: list[AccionPorParticipante] = Field(
        default_factory=list,
        description="Actividades asignadas a participantes.",
    )

class Temas_principales(BaseModel):
    temas: list[str] = Field(
        min_length=3,
        max_length=5,
        description='Temas principales discutidos'
        )


class Participantes(BaseModel):
    participantes: list[Participante] = Field(
        default_factory=list,
        description="Lista de participantes identificados en la reunión.",
    )


class Acciones(BaseModel):
    acciones: list[AccionPorParticipante] = Field(
        default_factory=list,
        description="Lista de acciones por participante identificadas en la reunión.",
    )