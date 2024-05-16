from typing import Optional


class BitMask:
    """
    Class to define a bit mask. For example, `BitMask(16, 32)` is for bits from [16, 32) => 0xffff0000.

    Attributes:
        offset (int): The starting bit position from the lowest bit, starts from zero, inclusive.
        mask (int): The bitmask calculated for the specified bit range.

    Examples:
        mask1 = BitMask(0, 16) # for bits from [0, 16) => 0xffff
        mask2 = BitMask(16, 32) # for bits from [16, 32) => 0xffff0000
        single_bit = BitMask(10) # for 10th bit [10, 11)
    """

    def __init__(self, start_bit: int, end_bit: Optional[int] = None) -> None:
        """
        Initializes a BitMask object with a specified range of bits. If only `start_bit` is provided,
        the mask will cover that single bit. `end_bit` must be greater than `start_bit`.

        Parameters:
            start_bit (int): Bit position from the lowest bit, starts from zero, inclusive.
            end_bit (Optional[int]): Bit position from the lowest bit, starts from zero, exclusive. Must be
                                     bigger than `startBit`. Defaults to `start_bit + 1` for a single bit mask.

        Raises:
            ValueError: If `start_bit` is not less than `end_bit`.
        """
        if end_bit is None:
            end_bit = start_bit + 1

        if not start_bit < end_bit:
            raise ValueError("BitMask: startBit must be less than endBit")

        self.offset = start_bit
        self.mask: int = (1 << (end_bit - start_bit)) - 1

    def __str__(self) -> str:
        """
        Returns the string representation of the bit mask in hexadecimal format.

        Returns:
            str: Hexadecimal string representation of the bit mask.
        """
        return f"0x{self.to_int():x}"

    def to_int(self) -> int:
        """
        Computes the bitmask value, adjusted by the offset.

        Returns:
            int: The bitmask represented as integer, shifted by the `offset`.
        """
        return self.mask << self.offset
