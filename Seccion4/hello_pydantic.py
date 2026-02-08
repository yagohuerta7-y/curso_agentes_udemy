from pydantic import BaseModel

# Definimos la estructura de los datos que queremos.
class Usuario(BaseModel):
    id: int
    nombre: str
    activo: bool = True
    
# Observa que los datos que estamos mandando no cumplen con las características de mi clase
data = {
    "id": "123",
    "nombre": "Ana"
}

# Transformamos a los datos usando mi clase
usuario = Usuario(**data) # Le pasamos los datos a la clase Usuario y esta se encarga de convertirlos al formato correcto

print(usuario.model_dump_json()) # Obligamos a que la salida sea unn JSON