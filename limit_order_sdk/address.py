from web3 import Web3
from limit_order_sdk.libs.byte_utils import add_0x


class Address:
    def __init__(self, val: str):
        assert Web3.is_address(val), f"Invalid address {val}"
        self.val = val.lower()

    @classmethod
    def from_int(cls, val: int) -> "Address":
        """Creates an Address instance from int value."""
        address: str = hex(val)[2:].zfill(40)
        return cls(add_0x(address))

    @classmethod
    def from_first_bytes(cls, bytes: str) -> "Address":
        """Creates an Address instance from the first bytes of a given string."""
        return cls(bytes[:42])

    def __str__(self) -> str:
        """Returns the string representation of the Address."""
        return self.val

    def equal(self, other: "Address") -> bool:
        """Checks if this Address is equal to another."""
        return self.val == other.val

    def is_native(self) -> bool:
        """Checks if this Address is the native currency address."""
        return self.equal(NATIVE_CURRENCY)

    def is_zero(self) -> bool:
        """Checks if this Address is the zero address."""
        return self.equal(ZERO_ADDRESS)


NATIVE_CURRENCY = Address("0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
ZERO_ADDRESS = Address("0x0000000000000000000000000000000000000000")
