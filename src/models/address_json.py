import os
import json 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class AddressJSON:
    def __init__(self):
        self.json_dict = {
            'vn': 'VietnamAdministrativeDivisions',
            'ph': 'AddressPhil',
            'th': 'AddressThai',
            'my': 'AddressMalay',
            'id': 'AddressIndo'
        }
        self.ads_dict = {
            'vn': ["provinces", 'districts', 'wards'],
            'ph': ["provName", 'cityName', 'areaName'],
            'th': ["provName", 'cityName', 'areaName'],
            'my': ["provName", 'cityName', 'areaName'],
            'id': ["province_name", 'city_name', 'district_name']            
        }

    def get_json(self, country_code='vn'):
        if country_code not in self.json_dict.keys():
            return {'error': 'Invalid country code.'}
        try:
            with open(os.path.join("assets", self.json_dict.get(country_code, None) +'.json'), 'r', encoding='utf_8') as file:
                address_json = json.load(file)
        except FileNotFoundError:
            address_json = {'error': 'JSON file not found.'}
        return address_json
    
    def get_ads(self, country_code='vn'):
        if country_code not in self.ads_dict.keys():
            return {'error': 'Invalid country code.'}
        return self.ads_dict.get(country_code, None)
