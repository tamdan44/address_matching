import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
import re
house_number_match = re.findall(r'\b\d+[A-Za-z]?\b', '18a/4 Nguyễn Văn Cừ, P. 4, Q. 5, TP. HCM')
print(house_number_match)