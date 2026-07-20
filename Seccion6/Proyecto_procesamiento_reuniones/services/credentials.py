import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


class Credentials:

    def __init__(self):
        load_dotenv()

        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        self.llm_model = ChatOpenAI(
            model="gpt-5-nano-2025-08-07",
            temperature=0,
            api_key=self.openai_api_key
        )

        if not self.openai_api_key:
            raise ValueError(
                "No se encontró OPENAI_API_KEY."
                "Agrégala a tu archivo .env"
            )