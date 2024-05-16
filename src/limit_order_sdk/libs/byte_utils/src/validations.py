import re

HEX_REGEX = re.compile(r"^(0x)[0-9a-f]+$", re.IGNORECASE)


def is_hex_string(val: str) -> bool:
    """
    Check that string starts with 0x and has only valid hex symbols.

    Parameters:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid hexadecimal string; False otherwise.
    """
    return bool(HEX_REGEX.match(val))


def is_hex_bytes(val: str) -> bool:
    """
    Check that string is a valid hex with 0x prefix and its length is even.

    Parameters:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid hexadecimal string with even length; False otherwise.
    """
    return is_hex_string(val) and len(val) % 2 == 0
