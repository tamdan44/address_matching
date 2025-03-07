import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

config = Config()
