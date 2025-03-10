import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import config
from src.models import AddressMatcher


matcher = AddressMatcher(llm_model="google")
matcher.get_output_address("123 Đường Lê Lai, Phường Bến Thành, Quận 1, TP Hồ Chí Minh, Việt Nam")



# matcher = AddressMatcher()
# # test cases 
# with open(os.path.join('assets','test_cases.txt'), 'r', encoding='utf_8') as file:
#     text = file.readlines()

# customer_address = [address.split('- Địa chỉ khách nhập: ')[1][:-1] for address in text if address.startswith('- Địa chỉ khách nhập: ')]
# true_address = [address.split('- Địa chỉ đơn hàng: ')[1][:-1] for address in text if address.startswith('- Địa chỉ đơn hàng: ')]
# old_ai = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]


# # create dataframe
# df = pd.DataFrame({'Old AI': old_ai, 'Customer Address': customer_address, 'True Address': true_address})
# df.drop_duplicates(inplace=True)
# old_ai = df['Old AI'].tolist()
# customer_address = df['Customer Address'].tolist()
# true_address = df['True Address'].tolist()

# # call get_output_address
# llm = load_llm(config.OPENAI_API_KEY, 0, "gpt-4-turbo-preview")

# ai_address = [matcher.get_output_address(llm, x) for x in customer_address]

# # process output
# new_address = [x.get('address', x.get('error', None)) if isinstance(x, dict) else None for x in ai_address]
# df['AI Address'] = new_address
# structured_address = [x.get('structured_address', None) if isinstance(x, dict) else None for x in ai_address]
# df['Structured Address'] = structured_address


# df.to_csv('test_cases.csv', index=True)


# country_codes = [x.get('country_code', None) if isinstance(x, dict) else None for x in structured_address]
# ids = [matcher.get_vn_address_id(structured_address[x]) if country_codes[x]=='vn' else matcher.get_foreign_address_id(structured_address[x], country_codes[x]) for x in range(len(new_address))]
# df['ID'] = ids

# # df = pd.DataFrame({'New AI': new_address, 'Error': error})

# df.to_csv('test_cases.csv', index=True)
    