from limit_order_sdk.libs.byte_utils.utils.zero_x_prefix import trim_0x


def get_bytes_count(hex_str: str) -> int:
    """
    Calculates the number of bytes in a hexadecimal string.

    Parameters:
        hex_str (str): The hexadecimal string.

    Returns:
        int: The count of bytes in the hexadecimal string.
    """
    return len(trim_0x(hex_str)) // 2
