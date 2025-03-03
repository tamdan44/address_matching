from address_utils import AddressMatcher
import pandas as pd
from llm_openai import load_llm
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import config


matcher = AddressMatcher()
# test cases 
with open(os.path.join('assets','test_cases.txt'), 'r', encoding='utf_8') as file:
    text = file.readlines()
customer_address = [address.split('- Địa chỉ khách nhập: ')[1][:-1] for address in text if address.startswith('- Địa chỉ khách nhập: ')]
true_address = [address.split('- Địa chỉ đơn hàng: ')[1][:-1] for address in text if address.startswith('- Địa chỉ đơn hàng: ')]
old_ai = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]


# create dataframe
df = pd.DataFrame({'Old AI': old_ai, 'Customer Address': customer_address, 'True Address': true_address})
df.drop_duplicates()

# call get_output_address
llm = load_llm(config.OPENAI_API_KEY, 0, "gpt-4-turbo-preview")

ai_address = [matcher.get_output_address(llm, x) for x in customer_address]

# process output
new_address = [x.get('address', x.get('error', None)) if isinstance(x, dict) else None for x in ai_address]
df['New AI'] = new_address
structured_address = [x.get('structured_address', None) if isinstance(x, dict) else None for x in ai_address]
df['Structured Address'] = structured_address


ids = [matcher.get_vn_address_id(new_address[x]) for x in range(len(new_address))]
df['ID'] = ids

# df = pd.DataFrame({'New AI': new_address, 'Error': error})

df.to_csv('test_cases.csv', index=True)
    