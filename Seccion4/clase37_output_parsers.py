# En forma muy resumida, pydantic lo que nos permite es procesar datos de origen, y validarlos, procesarlos y estructurarlos.

from pydantic import BaseModel


# Definimos nuestro modelo de datos personalizado
class Usuario(BaseModel):
    id: int
    nombre: str
    activo: bool = True
    

# Hagamos una prueba
data = {"id": "123", "nombre": "Ana"} # Aquí hace la conversión automática del id de str a int

usuario = Usuario(**data)
# print(usuario) # Esto imprime id=123 nombre='Ana' activo=True
print(usuario.model_dump_json()) # Este hace que nos retorne los datos como un JSON
