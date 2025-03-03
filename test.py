from address_utils import AddressMatcher
import pandas as pd
from dotenv import load_dotenv
from llm_utils import load_llm
import os

matcher = AddressMatcher()
# test cases 
with open('test_cases.txt', 'r', encoding='utf_8') as file:
    text = file.readlines()
customer_address = [address.split('- Địa chỉ khách nhập: ')[1][:-1] for address in text if address.startswith('- Địa chỉ khách nhập: ')]
true_address = [address.split('- Địa chỉ đơn hàng: ')[1][:-1] for address in text if address.startswith('- Địa chỉ đơn hàng: ')]
old_ai = [address.split('- AI chọn địa chỉ: ')[1][:-1] for address in text if address.startswith('- AI chọn địa chỉ: ')]


# create dataframe
df = pd.DataFrame({'Old AI': old_ai, 'Customer Address': customer_address, 'True Address': true_address})
df.drop_duplicates()

# call get_output_address
load_dotenv()
llm = load_llm(os.getenv("OPENAI_API_KEY"), 0, "gpt-4-turbo-preview")

ai_address = [matcher.get_output_address(llm, x) for x in customer_address]

    # process output
new_address = [x.get('address', x.get('error', None)) if isinstance(x, dict) else None for x in ai_address]
df['New AI'] = new_address


ids = [matcher.get_address_id(new_address[x]) for x in range(len(new_address))]
df['ID'] = ids

# df = pd.DataFrame({'New AI': new_address, 'Error': error})

df.to_csv('test_cases.csv', index=False)
    