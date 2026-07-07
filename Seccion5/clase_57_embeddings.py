import os
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


# Cargamos las variables de entorno
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Definimos el modelo de embeddings que vamos a usar
modelo_embeddings = OpenAIEmbeddings(
    model='text-embedding-3-small',
    # model='text-embedding-3-large',
    api_key=OPENAI_API_KEY
)

# Definimos los textos que vamos a comparar
t1 = 'La capital de Francia es Paris'
t2 = 'Paris es la ciudad capital de Francia'

# Hacemos sus embeddings
v1 = modelo_embeddings.embed_query(t1)
v2 = modelo_embeddings.embed_query(t2)

print(f'Dimension de los vectores de embeddings: {len(v1)}')


# Calculamos que tanto se parecen (Distancia coseno)
distancia = (np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

print(f'La distancia entre los vectores es de {distancia}')

# Imprime:
# Dimension de los vectores de embeddings: 1536
# La distancia entre los vectores es de 0.8464920020390421
