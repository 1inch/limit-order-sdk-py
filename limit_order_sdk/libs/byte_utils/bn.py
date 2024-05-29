from limit_order_sdk.libs.byte_utils.validations import is_hex_string
from limit_order_sdk.libs.byte_utils.utils.zero_x_prefix import add_0x
from limit_order_sdk.libs.byte_utils.bit_mask import BitMask


class BN:
    """
    Class to work with bits in number.
    Immutable, all methods return new value.

    Attributes:
        value (int): The numeric value of the number.

    Methods:
        from_number: Class method to create BN from a number.
        from_hex: Class method to create BN from a hex string.
        add: Add value to BN and return a new BN.
        sub: Subtract value from BN and return a new BN.
        set_bit: Set a specific bit to 1 or 0.
        get_bit: Get the value of a specific bit.
        shift_left: Shift the bits to the left.
        shift_right: Shift the bits to the right.
        and_op: Perform bitwise AND operation.
        or_op: Perform bitwise OR operation.
        xor_op: Perform bitwise XOR operation.
        is_zero: Check if the BN value is zero.
        is_one: Check if the BN value is one.
        get_mask: Return bits defined in `mask` as BN.
        set_mask: Set bits defined in `mask` to `value`.
        clear_mask: Set bits defined in `mask` to 0s.
        to_hex: Return 0x prefixed string with hex representation of BN.
        to_number: Convert BN to Number.
    """

    def __init__(self, value: int):
        """
        Initialize BN with a value.

        Args:
            value (int): The numeric value to initialize BN with.
        """
        self.value = value

    @classmethod
    def from_number(cls, n: int) -> "BN":
        """
        Class method to create BN from a number.

        Args:
            n (int): The number to create BN from.

        Returns:
            BN: A new BN instance.
        """
        return cls(n)

    @classmethod
    def from_hex(cls, hex_str: str) -> "BN":
        """
        Class method to create BN from a hex string.

        Args:
            hex_str (str): The hex string to create BN from.

        Returns:
            BN: A new BN instance.
        """
        assert is_hex_string(hex_str), "Invalid hex"
        return cls(int(hex_str, 16))

    # Other methods remain unchanged

    def to_hex(self, pad_num: int = 0) -> str:
        """
        Return 0x prefixed string with hex representation of BN,
        padded with '0s' if `padNum` specified.

        Args:
            pad_num (int, optional): Number of zeroes to pad. Defaults to 0.

        Returns:
            str: The hex representation of BN, optionally padded and prefixed with 0x.
        """
        return add_0x(hex(self.value)[2:].zfill(pad_num))

    def add(self, other: "BN") -> "BN":
        """
        Add value to this BN and return a new BN instance.

        Args:
            other (BN): The BN instance to add.

        Returns:
            BN: A new BN instance with the sum of this and other's values.
        """
        return BN(self.value + other.value)

    def sub(self, other: "BN") -> "BN":
        """
        Subtract a BN value from this BN and return a new BN instance.

        Args:
            other (BN): The BN instance to subtract.

        Returns:
            BN: A new BN instance with the difference of this and other's values.
        """
        return BN(self.value - other.value)

    def set_bit(self, n: int, value: int) -> "BN":
        """
        Set a specific bit to 1 or 0 and return a new BN instance.

        Args:
            n (int): The bit position to set.
            value (int): The value to set the bit to, either 1 or 0.

        Returns:
            BN: A new BN instance with the specified bit set.
        """
        if value:
            return BN(self.value | (1 << n))
        return BN(self.value & ~(1 << n))

    def get_bit(self, n: int) -> int:
        """
        Get the value of a specific bit.

        Args:
            n (int): The bit position to get.

        Returns:
            int: The value of the specified bit, either 1 or 0.
        """
        return 1 if (self.value & (1 << n)) else 0

    def shift_left(self, n: int) -> "BN":
        """
        Shift the bits to the left by n positions and return a new BN instance.

        Args:
            n (int): The number of positions to shift.

        Returns:
            BN: A new BN instance with the value shifted left.
        """
        return BN(self.value << n)

    def shift_right(self, n: int) -> "BN":
        """
        Shift the bits to the right by n positions and return a new BN instance.

        Args:
            n (int): The number of positions to shift.

        Returns:
            BN: A new BN instance with the value shifted right.
        """
        return BN(self.value >> n)

    def and_op(self, other: "BN") -> "BN":
        """
        Perform bitwise AND operation with another BN and return a new BN instance.

        Args:
            other (BN): The BN instance to perform the AND operation with.

        Returns:
            BN: A new BN instance as the result of the bitwise AND operation.
        """
        return BN(self.value & other.value)

    def or_op(self, other: "BN") -> "BN":
        """
        Perform bitwise OR operation with another BN and return a new BN instance.

        Args:
            other (BN): The BN instance to perform the OR operation with.

        Returns:
            BN: A new BN instance as the result of the bitwise OR operation.
        """
        return BN(self.value | other.value)

    def xor_op(self, other: "BN") -> "BN":
        """
        Perform bitwise XOR operation with another BN and return a new BN instance.

        Args:
            other (BN): The BN instance to perform the XOR operation with.

        Returns:
            BN: A new BN instance as the result of the bitwise XOR operation.
        """
        return BN(self.value ^ other.value)

    def is_zero(self) -> bool:
        """
        Check if the BN value is zero.

        Returns:
            bool: True if the BN value is zero, False otherwise.
        """
        return self.value == 0

    def is_one(self) -> bool:
        """
        Check if the BN value is one.

        Returns:
            bool: True if the BN value is one, False otherwise.
        """
        return self.value == 1

    def get_mask(self, mask: BitMask) -> "BN":
        """
        Return bits defined in `mask` as a new BN instance.

        Args:
            mask (BitMask): The bitmask to apply.

        Returns:
            BN: A new BN instance with bits defined by the mask.
        """
        shifted_value = self.shift_right(mask.offset).value
        return BN(shifted_value & mask.mask)

    def set_mask(self, mask: BitMask, value: int) -> "BN":
        """
        Set bits defined in `mask` to `value`. If value is bigger than mask, an error is thrown.

        Args:
            mask (BitMask): The bitmask to set bits within.
            value (int): The value to set within the mask.

        Returns:
            BN: A new BN instance with the mask applied.
        """
        assert value <= mask.mask, f"Value {hex(value)} too big for mask {mask} with mask value: {mask.mask}"
        cleared_value = self.clear_mask(mask).value
        return BN(cleared_value | (value << mask.offset))

    def clear_mask(self, mask: BitMask) -> "BN":
        """
        Set bits defined in `mask` to 0s and return a new BN instance.

        Args:
            mask (BitMask): The bitmask to clear bits within.

        Returns:
            BN: A new BN instance with the mask cleared.
        """
        return BN(self.value & ~mask.to_int())

    def to_number(self) -> int:
        """
        Convert BN to a Python integer.

        Caution: The value will be rounded for numbers greater than `Number.MAX_SAFE_INTEGER`.

        Returns:
            int: The integer representation of the BN value.
        """
        return int(self.value)
