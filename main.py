from address_utils import get_osm_address, get_output_address
from dotenv import load_dotenv
from llm_utils import load_llm
import os

load_dotenv()
llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")

if __name__ == "__main__":

    input_address = "Lot 9, Block 15, Jade St., Lorenville Subd., Mabini Hoomesite"
    final_address = get_output_address(llm, input_address)
    print("New AI:", final_address)

    # Nếu muốn lấy địa chỉ có structure
    # structured_address = get_output_address(input_address, structured=True)
    # print("Structured Address:", structured_address)