from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain.prompts import PromptTemplate


class LLMGoogle:
    def __init__(self, api_key: str, temp: float, model: str) -> ChatGoogleGenerativeAI:
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key, temperature=temp, model=model)

    def get_llm_address(self, input_address: str):
        """Uses LLM to extract structured address information."""
        
        prompt = PromptTemplate(
            input_variables=["input_address"],
            template='''You are an expert in address matching. Extract and return a JSON object with the address components.  
All of the addresses belong to one of the Southeast Asian countries. The input address is usually in English or Vietnamese.

### Instruction:
- The country_code are: {{"Vietnam": "vn", "Philipines": "ph", "Thailand": "th", "Indonesia": "id", "Malaysia": "my"}}.
- ad1 (first-level aministrative devision) might include tỉnh, thành phố trực thuộc trung ương (tp), province, region, NCR, etc.
- ad2 (second-level aministrative devision) might include quận, huyện, thành phố trực thuộc tỉnh (tp), thị xã, district, municipality, city, etc.
- ad3 (second-level aministrative devision) might include phường, xã, thị trấn (tt), subdistrict, ward, barangay, etc.
- ad2 (second-level aministrative devision) might include thôn, ấp, làng, village, community, zone, hamlet, etc. 
- street might include house numbers, street (st), đường, ngõ, hẻm, khu phố (kp), etc. 

### Example:
- Input: 18a Nguyễn Văn Cừ, P. 4, Q. 5, TP. HCM
- Output:
{{
"amenity": "",
"street": "18a Đường Nguyễn Văn Cừ",
"ad4": "",
"ad3": "Phường 4",
"ad2": "Quận 5",
"ad1": "Thành phố Hồ Chí Minh",
"country_code": "vn"
}}

- Input2: trường THCS Võ Thị Sáu Tổ 01 Thôn 5 Xã Tà Năng Lâm Đồng
- Output2:
{{
"amenity": "Trường THCS Võ Thị Sáu",
"street": "Tổ 01",
"ad4": "Thôn 5",
"ad3": "Xã Tà Năng",
"ad2": "",
"ad1": "Lâm Đồng",
"country_code": "vn"
}}

- Input3: Brgy. San Isidro General Santos City South Cotabato
- Output3:
{{
"amenity": "",
"street": "",
"ad4": "",
"ad3": "Barangay San Isidro",
"ad2": "General Santos City, South Cotabato",
"ad1": "",
"country_code": "ph"
}}

- Input4: #8 Luzon St, Marina Baytown East Gate 2
- Output4:
{{
"amenity": "Marina Baytown East Gate 2",
"street": "8 Luzon Street",
"ad4": "",
"ad3": "",
"ad2": "",
"ad1": "",
"country_code": "ph"
}}

### Input: {input_address}

### Output:
Ensure the output is a valid JSON object with:
- "amenity"
- "street"
- "ad4"
- "ad3"
- "ad2"
- "ad1"
- "country_code"'''
        )

        response = self.llm.invoke(prompt.format(input_address=input_address))
        
        try:
            address_data = json.loads(response.content.strip('```json\n').strip('```'))
            return address_data
        except json.JSONDecodeError:
            return response.content
