from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controllers import AddressController

router = APIRouter()

# Country choices
class CountryEnum(str, Enum):
    vn = "vn"
    th = "th"
    ph = "ph"
    my = "my"
    id = "id"

# Model choices
class ModelEnum(str, Enum):
    openai = "openai"
    google = "google"

# Request model
class AddressInput(BaseModel):
    user_input: str
    model: Optional[ModelEnum] = None 
    country_code: Optional[CountryEnum] = None 

# Initialize controller
global_controller = AddressController()

# Endpoints
@router.post("/get_address")
def get_address(input_data: AddressInput):
    global_controller.matcher.llm_model = input_data.model
    return global_controller.get_address(input_data.user_input)

@router.post("/get_address_id")
def get_address_id(input_data: AddressInput):
    global_controller.matcher.llm_model = input_data.model
    return global_controller.get_address_id(input_data.user_input, input_data.country_code)
