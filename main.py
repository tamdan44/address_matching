from address_utils import get_output_address, get_osm_address

if __name__ == "__main__":
    input_address = "Ngã Năm, An Tiến, Chí Hoà, Hưng Hà, Thái Bình"
    print(get_osm_address("Ngã Năm, An Tiến"))
    final_address = get_output_address(input_address)
    print("New AI:", final_address)

    # Nếu muốn lấy địa chỉ có structure
    # structured_address = get_output_address(input_address, structured=True)
    # print("Structured Address:", structured_address)