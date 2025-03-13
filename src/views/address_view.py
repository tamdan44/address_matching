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

# Request model
class AddressInput(BaseModel):
    user_input: str
    country_code: Optional[CountryEnum] = None 

# Initialize controller
controller = AddressController()

# Endpoints
@router.post("/get_address")
def get_address(input_data: AddressInput):
    return controller.get_address(input_data.user_input)

@router.post("/get_address_id")
def get_address_id(input_data: AddressInput):
    return controller.get_address_id(input_data.user_input, input_data.country_code)
