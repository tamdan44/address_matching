from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from address_utils import AddressMatcher
from llm_openai import load_llm

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import config, vn_json

# Initialize FastAPI app
app = FastAPI()
matcher = AddressMatcher()
llm = load_llm(config.OPENAI_API_KEY, 0, "gpt-4-turbo-preview")

# Request models
class AddressInput(BaseModel):
    user_input: str


# Endpoints
@app.post("/get_address")
def get_address(input_data: AddressInput):
    structured_address = matcher.get_output_address(llm, input_data.user_input)
    return structured_address

@app.post("/get_address_id")
def get_vn_address_id(input_data: AddressInput):
    structured_address = get_address(input_data)
    if 'error' in structured_address.keys():
        return structured_address
    return matcher.get_vn_address_id(vn_json, structured_address['address'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
