1. Giới thiệu

Xử lý địa chỉ do người dùng nhập, chuẩn hóa bằng mô hình ngôn ngữ (LLM) và truy xuất mã định danh địa điểm tương ứng.

2. Tổng quan

Được xây dựng bằng FastAPI và tích hợp cả mô hình LLM của OpenAI và Google để chuẩn hóa địa chỉ. Các thành phần chính bao gồm:

- FastAPI API (main.py): Cung cấp các endpoint cho hệ thống khớp địa chỉ.

- controllers (address_controller.py): Xử lý yêu cầu API và gọi logic khớp địa chỉ.

- models (address_json.py, address_utils.py, llm_google.py, llm_openai.py): Triển khai xử lý địa chỉ cốt lõi và tích hợp LLM.

- views(address_view.py, routes.py): Định nghĩa các API endpoints.

3. Chức năng chi tiết

3.1 main.py

- Khởi tạo app FastAPI.

- Đăng ký các tuyến API cho hệ thống Address Matching.

- Chạy API trên cổng 8000.

3.2 address_controller.py

- Triển khai class AddressController.

- Gọi AddressMatcher để xử lý địa chỉ thô và trả về kết quả chuẩn hóa.

- Các hàm chính:

	get_address(user_input: str): Trả về địa chỉ đã chuẩn hóa.

	get_address_id(user_input: str, country_code: str): Trả về mã định danh địa điểm từ địa chỉ chuẩn hóa.

3.3 address_view.py

- Định nghĩa các API endpoints để truy xuất địa chỉ.

- Sử dụng APIRouter để đăng ký tuyến đường.

- Hỗ trợ các quốc gia cụ thể (vn, th, ph, my, id).

Các endpoint chính:

- POST /get_address: Nhận địa chỉ từ người dùng và trả về phiên bản chuẩn hóa.

- POST /get_address_id: Nhận địa chỉ và mã quốc gia để truy xuất ID địa điểm tương ứng.

3.4 address_json.py

- Load JSON-based address mappings cho các quốc gia khác nhau.

3.5 address_utils.py

- Định nghĩa class AddressMatcher, chịu trách nhiệm xử lý address.

- Tương tác với cơ sở dữ liệu và LLM để tinh chỉnh chi tiết address.

3.6 llm_google.py & llm_openai.py

- Chuẩn hóa địa chỉ dựa trên LLM của Google và OpenAI.

- Nhận địa chỉ thô và trả về dưới dạng file JSON:
{
  "amenity": "",
  "street": "",
  "ad4": "",
  "ad3": "",
  "ad2": "",
  "ad1": "",
  "country_code": ""
}

4. Công nghệ sử dụng

- FastAPI: Framework xây dựng API.

- LangChain: Tích hợp với LLM.

- OpenAI & Google Generative AI: Chuẩn hóa địa chỉ.

- OpenStreetMaps: Database.

- Address Matching JSON: Xử lý địa chỉ theo từng quốc gia.

5. Chi phí

- Với Google API: Sử dụng model "gemini-2.0-flash" có cost $0.00001/1000 tokens

- Với ChatGPT API: Sử dụng model "gpt-4o-mini" có cost $0.00015/1000 tokens

-> Đặt mặc định là "gemini-2.0-flash"

6. Cải tiến

- Cải thiện xác thực địa chỉ với nhiều nguồn dữ liệu bên ngoài.

- Tăng hiệu suất với cơ chế lưu vào cache.

