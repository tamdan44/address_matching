from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import json


def load_llm(api_key: str, temp: float, model: str) -> ChatOpenAI:
    """Load the LLM model with the given API key and parameters."""
    return ChatOpenAI(openai_api_key=api_key, temperature=temp, model=model)


def get_llm_address(llm, input_address: str):
    """Uses LLM to extract structured address information."""
    
    prompt = PromptTemplate(
        input_variables=["input_address"],
        template='''You are an expert in address matching. Extract and return a JSON object with the address components.  
All of the addresses are in either Vietnam, Philipines or Thailand, so they might be written in the languages of those countries.
        
### Instruction:
- ad1 (first-level aministrative devision) might include tỉnh, thành phố trực thuộc trung ương, จังหวัด, กรุงเทพมหานคร, lalawigan/probinsya, NCR, etc.
- ad2 (second-level aministrative devision) might include quận, huyện, thành phố trực thuộc tỉnh, thị xã, อำเภอ, bayan, lungsod, etc.
- ad3 (second-level aministrative devision) might include phường, xã, thị trấn, ตำบล, เขต, barangay, etc.
- ad2 (second-level aministrative devision) might include thôn, ấp, làng, khu phố,

### Example:
- Input: 18a Nguyễn Văn Cừ, P. 4, Q. 5, TP. HCM
- Output:
{{
"amenity": "",
"street": "18a Đường Nguyễn Văn Cừ",
"ad4": "",
"ad3": "Phường 4",
"ad2": "QUuận 5",
"ad1": "Thành phố Hồ Chí Minh",
"country": "Vietnam"
}}

- Input2: trường THCS Võ Thị Sáu Tổ 01 Xã Tà Năng Lâm Đồng
- Output2:
{{
"amenity": "Trường THCS Võ Thị Sáu",
"street": "Tổ 01",
"ad4": "",
"ad3": "Xã Tà Năng",
"ad2": "",
"ad1": "Lâm Đồng",
}}

- Input3: 79 Nguyen Cong Trứ
- Output3:
{{
"Cơ sở": "",
"Đường": "79 Nguyen Cong Trứ",
"Phường": "",
"Xã": "",
"Quận": "",
"Huyện": "",
"Thành phố": "",
"Tỉnh": "",
"Deliverable": "No"
}}


- Input4: Sản Hai1xa Phuo Định Huyện Thh
- Output4:
{{
"Cơ sở": "Sản Hai1xa Phuo Định",
"Đường": "",
"Phường": "",
"Xã": "",
"Quận": "",
"Huyện": "Thh",
"Thành phố": "",
"Tỉnh": "",
"Deliverable": "No"
}}

### Input: {input_address}

### Output:
Ensure the output is a valid JSON object with:
- "Cơ sở"
- "Đường"
- "Phường"
- "Xã"
- "Quận"
- "Huyện"
- "Thành phố"
- "Tỉnh"
- "Deliverable"

If the address is not deliverable, return:
{{
"Cơ sở": "",
"Đường": "",
"Phường": "",
"Xã": "",
"Quận": "",
"Huyện": "",
"Thành phố": "",
"Tỉnh": "",
"Deliverable": "No"
}}
'''
    )

    response = llm(prompt.format(input_address=input_address))
    
    try:
        address_data = json.loads(response.content.strip('```json\n').strip('```'))
        return address_data
    except json.JSONDecodeError:
        return {"Error": "Invalid JSON response from LLM"}
