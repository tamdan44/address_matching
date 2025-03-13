
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.models import AddressMatcher

matcher = AddressMatcher()

class AddressController:
    @staticmethod
    def get_address(user_input: str):
        return matcher.get_output_address(user_input)

    @staticmethod
    def get_address_id(user_input: str, country_code: str):
        address = AddressController.get_address(user_input)
        if 'error' in address.keys():
            return address
        
        country_code = country_code or address['structured_address'].get('country_code')
        
        if country_code == 'vn':
            return matcher.get_vn_address_id(address['structured_address'])
        else:
            return matcher.get_foreign_address_id(address['structured_address'], country_code=country_code)
