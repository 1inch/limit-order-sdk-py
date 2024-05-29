from limit_order_sdk.libs.byte_utils.bytes_iter import BytesIter
from limit_order_sdk.libs.byte_utils.utils import trim_0x
from limit_order_sdk.libs.byte_utils.validations import is_hex_bytes
from limit_order_sdk.address import Address


class Interaction:
    """
    Create `Interaction` from bytes
    @param bytes Hex string with 0x. First 20 bytes are target, then data
    """

    def __init__(self, target: Address, data: str):
        assert is_hex_bytes(data), "Interaction data must be valid hex bytes"
        self.target = target
        self.data = data

    @staticmethod
    def decode(bytes: str) -> "Interaction":
        iter = BytesIter.string(bytes)
        target = Address(iter.next_uint160())
        data = iter.rest()
        return Interaction(target, data)

    # Hex string with 0x. First 20 bytes are target, then data
    def encode(self) -> str:
        return str(self.target) + trim_0x(self.data)

    def __repr__(self):
        return f"Interaction(target={self.target}, data={self.data})"
