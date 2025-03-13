import requests
import re
from unidecode import unidecode

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from configs import config
from src.models.address_json import AddressJSON
from src.models.llm_openai import LLMOpenAI
from src.models.llm_google import LLMGoogle


class AddressMatcher:
    def __init__(self, user_agent="AdressMatching/1.0", country_codes=['vn', 'ph', 'th', 'my', 'id']):
        self.base_url = config.DATABASE_URL
        self.headers = {"User-Agent": user_agent}
        self.country_codes = country_codes
        self.llm = self.load_llm(temp=0)

    def load_llm(self, temp):
        return LLMGoogle(config.GOOGLE_API_KEY, temp=temp, model="gemini-2.0-flash") #0.00001

    def get_osm_address(self, input_address):
        """Lấy địa chỉ bằng API OpenStreetMap Nominatim."""
        if isinstance(input_address, dict):
            return input_address['error']
        params = {
            "q": input_address,
            "format": "json",
            "addressdetails": 1,
            "limit": 1,
        }

        response = requests.get(self.base_url, params=params, headers=self.headers)

        if response.status_code == 200 and response.json():
            data = response.json()[0]["address"]
            print(data)
            if data['country_code'] not in self.country_codes:
                return None, None

            address = {
                "amenity": data.get("amenity", data.get('tourism', data.get('historic', ''))),

                "street": " ".join(filter(
                    None, [data.get("house_number", ""), data.get("road", data.get("street", "")), data.get("water", "")]
                    )),

                "ad4":  ", ".join(filter(
                    None, [data.get("hamlet", data.get('borough', data.get('neighbourhood', ""))), data.get("quarter", data.get("village", ""))]
                    )),

                "ad3": data.get("town", data.get('ward', data.get('subdistrict', ""))),

                "ad2": ", ".join(filter(
                    None, [data.get("region", data.get('suburb', "")), data.get("city_district", data.get("county", data.get("district", "")))]
                    )),
                
                "ad1": ", ".join(filter(
                    None, [data.get("city", ""), data.get("state", data.get("state_district", ""))]
                    )),
                "country": data.get("country", "")
            }
            return address, data
        return None, None


    def format_address(self, structured_address: dict, drop=["amenity", "street", "country_code"]):
        if isinstance(structured_address, str):
            return structured_address
        filtered_items = {k: v for k, v in structured_address.items() if v!=''}
        return ", ".join([v for k, v in filtered_items.items() if k not in drop])

    def is_deliverable(self, structured_address: dict, hard_check=False):
        """Check if address is deliverable."""
        filtered_items = {k: v for k, v in structured_address.items() if v!=''}
        keys = list(filtered_items.keys())
        if len(keys) <=2 or (len(keys)<=4 and 'ad1' not in keys and 'ad2' not in keys and 'ad3' not in keys):
            return False
        if hard_check and len(keys)<=4 and 'ad1' not in keys and 'ad2' not in keys and ('ad3' not in keys or 'ad4' not in keys):
            return False
        return True

    def is_madeup_address(self, llm_address, output_address):
        """Check if llm_address is made up."""
        llm_items_num = len({k: v for k, v in llm_address.items() if v!=''})
        print('num', llm_items_num<=5)
        if llm_address.get("amenity", "") == "" and (not output_address.get("amenity", "") == "") and llm_items_num<=5:
            return True
        return False

    def get_output_address(self, input_address):
        """Trả về địa chỉ output, kết hợp OpenStreetMap và LLM."""

        input_address = " ".join(input_address.split())
        dropped = ["amenity", "country_code"]

        # LLM
        llm_address = self.llm.get_llm_address(input_address)
        if not self.is_deliverable(llm_address):
            return {'error': 'The address is not clear enough for delivery. Please add more details.'}

        for replace_key in ["amenity", "street"]:
            if len(llm_address.get(replace_key, "").split()) <=2 and llm_address.get("country_code", "") == 'vn':
                llm_address["ad4"] = llm_address[replace_key] + ' ' + llm_address["ad4"]
                llm_address[replace_key] = ""
        print(llm_address)

        llm_items = {k: v for k, v in llm_address.items() if v!=''}

        # OpenStreetMap
        osm_address, structured_address = self.get_osm_address(self.format_address(llm_address, drop=[]))
        if osm_address and self.is_madeup_address(llm_address, osm_address):
            osm_address = None
            
        if not osm_address:
            print(2)
            if not self.is_deliverable(llm_address, hard_check=True):
                return {'error': 'Address not found. Please try again.'}
            formatted_address = self.format_address(llm_address, drop=dropped)
            osm_address, structured_address = self.get_osm_address(formatted_address) or self.get_osm_address(formatted_address.lower().replace('city', '').replace('barangay', ''))
            if osm_address and self.is_madeup_address(llm_address, osm_address):
                osm_address = None

        for drop_key in ["street", "ad4", "ad3"]:
            if not osm_address:
                print(3)
                dropped.append(drop_key)
                osm_address, structured_address = self.get_osm_address(self.format_address(llm_address, drop=dropped))
                if osm_address and self.is_madeup_address(llm_address, osm_address):
                    print('madeup', osm_address)
                    osm_address = None
                elif osm_address:
                    break

        if not osm_address:
            print(4)
            osm_address, structured_address = self.get_osm_address(input_address)
            if osm_address and not self.is_madeup_address(llm_address, osm_address):
                if self.is_madeup_address(llm_address, osm_address):
                    return {'error': 'The address is not clear enough for delivery. Please add more details.'}
                output_address = self.format_address(osm_address)

                house_number = re.search(r'\b\d+[A-Za-z]?([\/-]\d+)*\b', input_address)
                if house_number and house_number not in output_address:
                    output_address = house_number + ', ' + output_address
                return {'address': output_address, 'structured_address':structured_address}
            
        if not osm_address:
            return {'error': 'Address not found. Please try again.'}

        # Kết hợp into output
        output_address = ""
        dropped.remove("country_code")
        for x in dropped:
            if x in llm_items:
                output_address += llm_address.get(x, "").strip() + ", "
        output_address += self.format_address(osm_address, drop=[])

        return {'address': output_address, 'structured_address': structured_address}

    def get_vn_address_id(self, structured_address):
        if isinstance(structured_address, dict) and structured_address.get('country_code', None) == 'vn':
            structured_address.pop('country_code')
            structured_address.pop('country')
            address_components = list(structured_address.values())
        else:
            return None
        
        address_components.reverse()
        if 'Huế' in address_components[1]:
            address_components[1] = 'Thừa Thiên Huế'

        vn_dict = AddressJSON().get_json('vn')
        if vn_dict.get('error', None):
            return vn_dict
        location_list = vn_dict.get("provinces", None)

        ads =["provinces", 'districts', 'wards']
        ad = 0
        id = None
        name = []
        for address_component in address_components:
            index = self.find_index(location_list, address_component)
            print(address_component)
            if index is not None:
                name.append(location_list[index]['name'])
                id = location_list[index]['id']
                ad+=1
                try:
                    location_list = location_list[index][ads[ad]]
                except IndexError:
                    break
        name.reverse()
        return {'id': id, 'level': ads[ad-1], 'name': ' - '.join(name)}

    def get_foreign_address_id(self, structured_address, country_code='ph'):
        if isinstance(structured_address, dict) and structured_address.get('country_code', None) == country_code:
            structured_address.pop('country_code')
            structured_address.pop('country')
            address_components = list(structured_address.values())
        else:
            return None
        
        address_components.reverse()
        address_components = [unidecode(x) for x in address_components]

        prov_dicts = AddressJSON().get_json(country_code)
        if isinstance(prov_dicts, dict):
            return prov_dicts

        count = 0
        ids = {}
        for address_component in address_components:
            if count==0:
                city_dicts = [x for x in prov_dicts if address_component.lower() in x.get("provName", None).replace('-',' ').lower()]
                if len(city_dicts)>0:
                    count+=1
                    ids["provId"] = city_dicts[0].get("provId", None)
                    ids["provName"] = city_dicts[0].get("provName", None)
                continue 

            if count==1:
                area_dicts = [x for x in city_dicts if address_component.split(' ')[-1].lower() in x.get("cityName", None).replace('-',' ').lower()]
                if len(area_dicts)>0:
                    count+=1
                    ids["cityId"] = area_dicts[0].get("cityId", None)
                    ids["cityName"] = area_dicts[0].get("cityName", None)
                continue 

            if count==2:
                area = [x for x in area_dicts if address_component.split(' ')[-1].lower() in x.get("areaName", None).replace('-',' ').lower()]
                if len(area)==1:
                    return area[0]
        if count>0:
            return ids
        return None

    @staticmethod
    def find_index(dict_list: list[dict], query: str):
        """Tìm index của query trong list of dictionary."""
        name_list = [x['name'] for x in dict_list]
        query = query.strip()
        for i, name in enumerate(name_list):
            location = ' '.join(name.split()[-2:])
            if unidecode(location).lower() in unidecode(query).lower():
                return i
        return None