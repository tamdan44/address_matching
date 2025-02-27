from address_utils import get_osm_address, get_output_address
import pandas as pd
from dotenv import load_dotenv
from llm_utils import load_llm
import os

# test cases 1
# with open('test_case.txt', 'r', encoding='utf_8') as file:
#     text = file.readlines()
# customer_address1 = [address.split('- Khách nhập: ')[1][:-1] for address in text if address.startswith('- Khách nhập:')]
# old_ai1 = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]
# true_address1 = [None]*len(old_ai1)
customer_address1 = []
old_ai1 = []
true_address1 = []


# test cases 2
with open('test_case_2.txt', 'r', encoding='utf_8') as file:
    text = file.readlines()
customer_address2 = [address.split('- Địa chỉ khách nhập: ')[1][:-1] for address in text if address.startswith('- Địa chỉ khách nhập: ')]
true_address2 = [address.split('- Địa chỉ đơn hàng: ')[1][:-1] for address in text if address.startswith('- Địa chỉ đơn hàng: ')]
old_ai2 = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]


# create dataframe
df = pd.DataFrame({'Customer Address': customer_address2+customer_address1, 'True Address': true_address2+true_address1, 'Old AI':old_ai2+old_ai1})

# call get_output_address
load_dotenv()
llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")

customer_address = customer_address2+customer_address1
ai_address =[get_output_address(llm, x) for x in customer_address]

    # process output
new_address = [x.get('address', None) if isinstance(x, dict) else x for x in ai_address]
error = [x.get('error', None) if isinstance(x, dict) else None for x in ai_address]

df['New AI'] = new_address
df['Error'] = error
df.to_csv('test_cases.csv', index=False)
    