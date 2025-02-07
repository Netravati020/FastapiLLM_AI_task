from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_KEY = os.getenv("API_KEY")  # Load FastAPI Authentication Key

    DEBUG = os.getenv("DEBUG", False)

config = Config()
