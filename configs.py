import os
from dotenv import load_dotenv
import json 

load_dotenv()  

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

try:
    with open(os.path.join("assets", 'VietnamAdministrativeDivisions.json'), 'r', encoding='utf_8') as file:
        vn_json = json.load(file)
except FileNotFoundError:
    vn_json = {'error': 'File not found.'}

config = Config()
