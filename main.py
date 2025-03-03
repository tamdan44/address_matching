from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from address_utils import AddressMatcher
from llm_utils import load_llm
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()
matcher = AddressMatcher()
load_dotenv()
llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")

# Request models
class AddressInput(BaseModel):
    user_input: str


# Endpoints
@app.post("/get_address")
def get_address(input_data: AddressInput):
    return matcher.get_output_address(llm, input_data.user_input)

@app.post("/get_address_id")
def get_address_id(input_data: AddressInput):
    structured_address = matcher.get_output_address(llm, input_data.user_input)
    if 'error' in structured_address.keys():
        return structured_address
    return matcher.get_address_id(structured_address['address'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
