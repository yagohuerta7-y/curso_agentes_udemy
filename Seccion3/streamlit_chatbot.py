import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st

# Cargamos la variable de entorno de la api key
load_dotenv()

# Asignamos la api key a la variable de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuramos la página de la app
st.set_page_config(page_title="Chat de Yago", page_icon="😈")
st.title("Chat de Yago usando langchain")
st.markdown("Este es un pequeño ejemplo de un chat con langchain en streamlit")


# Definimos el modelo de IA que vamos a usar
ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.0, api_key=OPENAI_API_KEY)