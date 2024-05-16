def trim_0x(data: str) -> str:
    """
    Removes the '0x' prefix from a string if it starts with '0x'.

    Parameters:
        data (str): The string to trim.

    Returns:
        str: The trimmed string without the '0x' prefix.
    """
    if data.startswith("0x"):
        return data[2:]
    return data


def add_0x(data: str) -> str:
    """
    Adds a '0x' prefix to a string if it doesn't already include '0x'.

    Parameters:
        data (str): The string to modify.

    Returns:
        str: The modified string with a '0x' prefix if it was missing.
    """
    if not data.startswith("0x"):
        return "0x" + data
    return data
