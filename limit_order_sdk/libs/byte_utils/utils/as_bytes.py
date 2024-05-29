def as_bytes(val: int) -> str:
    """
    Formats `val` as 0x prefixed string with even length.

    Parameters:
        val (int): The integer value to format as a hexadecimal string.

    Returns:
        str: The formatted hexadecimal string with 0x prefix and even length.
    """
    hex_str = hex(val)[2:]  # Convert to hex and remove the '0x' prefix

    if len(hex_str) % 2:
        return "0x0" + hex_str

    return "0x" + hex_str
