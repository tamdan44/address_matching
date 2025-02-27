import requests
import os
import re
import json
from llm_utils import load_llm, get_llm_address


def get_osm_address(input_address):
    """Lấy địa chỉ bằng API OpenStreetMap Nominatim."""
    if isinstance(input_address, dict):
        return input_address['error']
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": input_address,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    response = requests.get(base_url, params=params, headers={"User-Agent": "YourApp/1.0"})

    if response.status_code == 200 and response.json():
        data = response.json()[0]["address"]
        country_codes = ['vn', 'ph', 'th']
        print(data)
        if data['country_code'] not in country_codes:
            return None

        structured_address = {
            "amenity": data.get("amenity", data.get('neighbourhood', data.get('water', ""))),

            "street": " ".join(filter(
                None, [data.get("house_number", ""), data.get("road", data.get("street", ))]
                )),

            "ad4":  ", ".join(filter(
                None, [data.get("hamlet", data.get('borough', "")), data.get("quarter", data.get("village", ""))]
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
        return structured_address
    return None


def format_address(structured_address, full=False):
    if isinstance(structured_address, str):
        return structured_address
    filtered_items = {k: v for k, v in structured_address.items() if v!=''}
    if full:
        parts = [v for k, v in filtered_items.items() if k != "country_code"]
    else:
        parts = [v for k, v in filtered_items.items() if k not in ["amenity", "street", "country_code"]]

    return ", ".join(parts)

def is_deliverable(structured_address, check_one=False):
    filtered_items = {k: v for k, v in structured_address.items() if v!=''}
    if not check_one:
        if (filtered_items.get('ad1', '')=='') and (filtered_items.get('ad2', '')=='' or filtered_items.get('ad3', '')==''):
            return False
    else:
        if len(filtered_items) <=2 or ["amenity", "street", "country_code"] == list(filtered_items.keys()):
            return False
    return True

def get_output_address(llm, input_address):
    """Trả về địa chỉ output, kết hợp OpenStreetMap và LLM."""

    input_address = " ".join(input_address.split())

    # LLM
    llm_address = get_llm_address(llm, input_address)
    if not is_deliverable(llm_address, check_one=True):
        return {'error': 'The address is not clear enough for delivery. Please add more details.', 'address': llm_address}

    filtered_items = {k: v for k, v in llm_address.items() if v!=''}
    print(format_address(llm_address))


        # OpenStreetMap
    osm_address = None
    if len(filtered_items)<=3:
        osm_address = get_osm_address(format_address(llm_address, full=True))

    if not osm_address:
        osm_address = get_osm_address(format_address(llm_address))

    if not osm_address:
        osm_address = get_osm_address(input_address)

        if osm_address:
            output_address = format_address(osm_address)
                # if llm_address.get("street", '') != '':
                #     output_address = llm_address['street'] + ', ' + output_address
                # if llm_address.get("amenity", '') != '':
                #     output_address = llm_address['amenity'] + ', ' + output_address

            house_number = re.search(r'\b\d+[A-Za-z]?([\/-]\d+)*\b', input_address)
            if house_number and house_number not in output_address:
                output_address = house_number + ', ' + output_address
            return {'address': output_address}
            
        return {'error': 'Address not found. Please try again.', 'address': osm_address}

    if not is_deliverable(osm_address):
        return {'error': 'The address is not clear enough for delivery. Please add more details.', 'address': osm_address}

    # Kết hợp into output
    output_address = ", ".join(filter(None, [
        llm_address.get("amenity", ""),
        llm_address.get("street", ""),
        format_address(osm_address, full=True)
    ]))

    return output_address