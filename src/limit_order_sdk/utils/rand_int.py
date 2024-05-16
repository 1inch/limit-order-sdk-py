from typing import Union
import secrets


def rand_int(max: Union[int, float]) -> int:
    """
    Generates a random integer within the range [0, max].

    Args:
        max (Union[int, float]): The maximum value (inclusive) the generated number could be. Can be int or float.

    Returns:
        int: A random integer within the specified range.
    """
    max = int(max) + 1
    bytes_count = 0
    rest = max
    while rest:
        rest = rest >> 8
        bytes_count += 1

    # Generate a random byte sequence of the determined length.
    bytes_seq = secrets.token_bytes(bytes_count)

    # Convert the byte sequence to an int.
    val = int.from_bytes(bytes_seq, byteorder="little")

    return val % max
