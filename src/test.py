import pandas as pd
import os
import sys
import ast
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import config
from src.models import AddressMatcher



matcher = AddressMatcher()
# # test cases 
# with open(os.path.join('assets','test_cases.txt'), 'r', encoding='utf_8') as file:
#     text = file.readlines()

# customer_address = [address.split('- Địa chỉ khách nhập: ')[1][:-1] for address in text if address.startswith('- Địa chỉ khách nhập: ')]
# true_address = [address.split('- Địa chỉ đơn hàng: ')[1][:-1] for address in text if address.startswith('- Địa chỉ đơn hàng: ')]
# old_ai = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]


# create dataframe
df = pd.read_csv('test_cases.csv')
df.drop_duplicates(inplace=True)

structured_address = df['Structured Address'].tolist()
structured_address = [ast.literal_eval(x) if isinstance(x, str) else None for x in structured_address]

# old_ai = old_ai[len(df['Old AI']):]
# customer_address = customer_address[len(df['Customer Address']):]
# true_address = true_address[len(df['True Address']):]


# call get_output_address

# ai_address = [matcher.get_output_address(llm, x) for x in customer_address]

# # process output
# new_address = [x.get('address', x.get('error', None)) if isinstance(x, dict) else None for x in ai_address]
# df['AI Address'] = new_address
# structured_address = [x.get('structured_address', None) if isinstance(x, dict) else None for x in ai_address]
# df['Structured Address'] = structured_address


# df.to_csv('test_cases.csv', index=True)

country_codes = [x.get('country_code', None) if isinstance(x, dict) else None for x in structured_address]
print(set(country_codes))
ids = [matcher.get_vn_address_id(structured_address[x]) if country_codes[x]=='vn' else matcher.get_foreign_address_id(structured_address[x], country_code=country_codes[x]) for x in range(len(country_codes))]
df['ID'] = ids
df = df[['Old AI', 'Customer Address', 'True Address', 'AI Address', 'Structured Address', 'ID']]


df.to_csv('test_cases.csv', index=True)
    