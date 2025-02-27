import requests
import os
import re
import json
from dotenv import load_dotenv
from llm_utils import load_llm, get_llm_address


def get_osm_address(input_address):
    """Lấy địa chỉ bằng API OpenStreetMap Nominatim."""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": input_address.strip(),
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    response = requests.get(base_url, params=params, headers={"User-Agent": "YourApp/1.0"})

    if response.status_code == 200 and response.json():
        data = response.json()[0]["address"]
        print(data)

        structured_address = {
            "Cơ sở": data.get("amenity", data.get('neighbourhood', "")),
            "Đường": " ".join(filter(None, [data.get("house_number", ""), data.get("road", "")])),
            "Phường/Xã": data.get("quarter", data.get("village", data.get('borough', ""))),
            "Quận/Huyện": data.get("city_district", data.get("county", data.get("suburb", data.get("district", "")))),
            "Thành phố": data.get("city", data.get('town', "")),
            "Tỉnh": data.get("state", data.get("state_district", )),
            "Quốc gia": data.get("country", "")
        }
        return structured_address
    return None


def format_address(llm_address):
    if "Error" in llm_address:
        return {"Error": llm_address["Error"]}

    filtered_items = {k: v for k, v in llm_address.items() if v}

    parts1 = [f"{k} {v}" for k, v in filtered_items.items() if k not in ["Cơ sở", "Đường", "Deliverable"]]
    parts2 = [v for k, v in filtered_items.items() if k not in ["Cơ sở", "Đường", "Deliverable"]]

    return ", ".join(parts1), ", ".join(parts2)


def get_output_address(input_address, structured = False):
    """Trả về địa chỉ output, kết hợp OpenStreetMap và LLM."""

    # LLM
    load_dotenv()
    llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")
    llm_address = get_llm_address(llm, input_address)

    if llm_address["Deliverable"] == "No":
        return {"Error": "Địa chỉ giao hàng chưa rõ ràng. Xin hãy nhập lại và lưu ý chính tả.", "Address Invalid": input_address}

    try:
        formatted_address1, formatted_address2 = format_address(llm_address)
    except:
        return format_address(llm_address)

    # OpenStreetMap
    osm_address = get_osm_address(input_address) or get_osm_address(formatted_address1) or get_osm_address(formatted_address2) 

    if not osm_address:
        if get_osm_address(llm_address["Tỉnh"] + ", " + llm_address["Thành phố"]):
            return input_address
        return {"Error": "Địa chỉ giao hàng chưa rõ ràng. Xin hãy nhập lại và lưu ý chính tả.", "Address Invalid": input_address}

    # Kết hợp into output
    if structured:
        osm_address.update({
            "Cơ sở": llm_address.get("Cơ sở", ""),
            "Đường": llm_address.get("Đường", "")
        })
        return osm_address

    if not isinstance(osm_address, str):
        output_address = ", ".join(filter(None, [
            llm_address.get("Cơ sở", ""),
            llm_address.get("Đường", ""),
            ", ".join(value for value in osm_address.values() if value and value!='')
        ]))
    else:
        output_address = ", ".join(filter(None, [
            llm_address.get("Cơ sở", ""),
            llm_address.get("Đường", ""),
            ", ", osm_address
        ]))

    return output_address