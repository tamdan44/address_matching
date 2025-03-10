
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.models import AddressMatcher


class AddressController:
    def __init__(self, model: str = "openai"):
        self.matcher = AddressMatcher(llm_model=model)

    def get_address(self, user_input: str):
        return self.matcher.get_output_address(user_input)

    def get_address_id(self, user_input: str, country_code: str):
        address = self.get_address(user_input)
        if 'error' in address.keys():
            return address
        
        country_code = country_code or address['structured_address'].get('country_code')
        
        if country_code == 'vn':
            return self.matcher.get_vn_address_id(address['structured_address'])
        else:
            return self.matcher.get_foreign_address_id(address['structured_address'], country_code=country_code)
