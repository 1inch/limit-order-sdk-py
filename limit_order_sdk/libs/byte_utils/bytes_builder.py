from limit_order_sdk.libs.byte_utils.utils import trim_0x
from limit_order_sdk.libs.byte_utils.bn import BN
from limit_order_sdk.libs.byte_utils.constants import UINT_160_MAX
from limit_order_sdk.libs.byte_utils.validations import is_hex_bytes


class BytesBuilder:
    """
    Helper class to build an arbitrary bytes sequence. It supports initialization from string, BN, or int,
    and provides methods to add various types of data to the bytes sequence.
    """

    def __init__(self, init=None):
        """
        Initializes the bytes sequence.

        Args:
            init (Optional[str, BN, int]): Initial value to set the bytes sequence to. Can be a hex string,
            a BN object, or a int. If None, initializes to "0x".
        """
        if init is None:
            self.bytes = "0x"
        else:
            if isinstance(init, str):
                assert is_hex_bytes(init), "Init bytes must be valid hex bytes"
                self.bytes = init
            else:
                init_bn = init if isinstance(init, BN) else BN(init)
                self.bytes = init_bn.to_hex()

    @property
    def length(self):
        # Returns current bytes count
        return (len(self.bytes) // 2) - 1

    def add_address(self, address):
        # Adds an address, validating it if it's a string or using BN/int
        if isinstance(address, str):
            assert is_hex_bytes(address) and len(address) == 42, "Invalid address"
            self.append(address)
        else:
            address_bn = address if isinstance(address, BN) else BN(address)
            assert address_bn.value <= UINT_160_MAX, "Invalid address: too big"
            self.append(address_bn.to_hex(40))
        return self

    def add_bytes(self, bytes_str):
        # Adds arbitrary bytes, must be a valid hex string
        assert is_hex_bytes(bytes_str), "Invalid bytes"
        self.append(bytes_str)
        return self

    # Add a single byte, validating it's in proper hex format
    def add_byte(self, byte):
        return self.add_n_bytes(byte, 1)

    # Methods for adding numeric values with specific byte lengths
    def add_uint8(self, val):
        return self.add_n_bytes(val, 1)

    def add_uint16(self, val):
        return self.add_n_bytes(val, 2)

    def add_uint24(self, val):
        return self.add_n_bytes(val, 3)

    def add_uint32(self, val):
        return self.add_n_bytes(val, 4)

    def add_uint64(self, val):
        return self.add_n_bytes(val, 8)

    def add_uint128(self, val):
        return self.add_n_bytes(val, 16)

    def add_uint160(self, val):
        return self.add_n_bytes(val, 20)

    def add_uint256(self, val):
        return self.add_n_bytes(val, 32)

    def as_int(self):
        # Returns bytes as single int value
        return int(self.bytes, 16)

    def as_hex(self, prefixed=True):
        # Returns hex string, optionally prefixed with 0x
        return self.bytes if prefixed else self.bytes[2:]

    def append(self, bytes_str):
        # Appends hex bytes, removing the 0x prefix if present
        self.bytes += trim_0x(bytes_str)

    def add_n_bytes(self, bytes, n):
        """
        Adds a value as N bytes to the bytes sequence. This method supports adding the value as a hex string,
        a BN object, or int. It automatically handles padding and ensures the value fits within the specified
        number of bytes.

        Args:
            bytes (str, BN, int): The value to add. If a string, it must be a valid hex string.
            n (int): The number of bytes the value should occupy.

        Returns:
            self: To allow for method chaining.

        Raises:
            AssertionError: If the value cannot be represented in N bytes or if a string value is not a valid hex string.
        """
        if isinstance(bytes, str):
            assert is_hex_bytes(bytes), "Invalid value: not bytes hex string"
            assert len(trim_0x(bytes)) == n * 2, "Invalid value: bad length"
            self.append(bytes)
        else:
            bytes_bn = bytes if isinstance(bytes, BN) else BN(bytes)
            # Ensure the int value can fit in n bytes
            max_value = (1 << (8 * n)) - 1
            assert bytes_bn.value <= max_value, "Invalid value: too long"
            # Convert the BN/int to a hex string, padding it to fit exactly n bytes
            self.append(bytes_bn.to_hex(pad_num=n * 2))
        return self
