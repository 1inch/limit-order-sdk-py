def is_int(val) -> bool:
    """
    Checks if the given value is an integer.

    Args:
        val: The value to check.

    Returns:
        bool: True if val is an integer, False otherwise.
    """
    return isinstance(val, int) or (isinstance(val, float) and val.is_integer())
