from address_utils import AddressUtils
from dotenv import load_dotenv
from llm_utils import load_llm
import os

load_dotenv()
llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")

if __name__ == "__main__":
    utils = AddressUtils()
    input_address = "Số Nhà 137,tổ 5 Khu Gia Mô Phường Kim Sơn"
    final_address = utils.get_output_address(llm, input_address)
    print("New AI:", final_address)

    # Nếu muốn lấy địa chỉ có structure
    # structured_address = get_output_address(input_address, structured=True)
    # print("Structured Address:", structured_address)