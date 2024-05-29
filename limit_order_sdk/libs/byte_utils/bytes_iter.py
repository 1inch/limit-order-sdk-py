from typing import Callable, Any
from limit_order_sdk.libs.byte_utils.validations import is_hex_bytes
from limit_order_sdk.libs.byte_utils.utils.zero_x_prefix import add_0x


class Side:
    Front = "Front"
    Back = "Back"


# Class to iterate through bytes string by parsing individual bytes
# Example usage:
# iter = BytesIter[int]('0xdeadbeef', int)
# byte1 = iter.next_byte()  # Returns int(0xde)
# byte2 = iter.next_byte()  # Returns int(0xad)
# bytes34 = iter.next_bytes(2)  # Returns int(0xbeef)
class BytesIter:

    def __init__(self, bytes: str, result_type: Callable[[str], Any]):
        assert is_hex_bytes(bytes), "invalid bytes value"
        self.bytes = bytes[2:]  # trim 0x
        self.result_type = result_type

    @classmethod
    def to_int(cls, bytes: str) -> "BytesIter":
        # base=0 automatically adapts to given bytes, so no need to specify base (16, 10, 8, etc.)
        return cls(bytes, lambda b: int(b, base=0))

    @classmethod
    def string(cls, bytes: str) -> "BytesIter":
        return cls(bytes, str)

    # Returns all not consumed bytes
    def rest(self) -> Any:
        return self.result_type(add_0x(self.bytes))

    def is_empty(self) -> bool:
        return len(self.bytes) == 0

    def next_byte(self, side: str = Side.Front) -> Any:
        return self.next_bytes(1, side)

    def next_bytes(self, n: int, side: str = Side.Front) -> Any:
        cnt = n * 2
        if len(self.bytes) < cnt:
            raise ValueError(f"Cannot consume {n} bytes, have only {len(self.bytes) // 2}")

        is_front = side == Side.Front
        bytes = self.bytes[:cnt] if is_front else self.bytes[-cnt:]
        self.bytes = self.bytes[cnt:] if is_front else self.bytes[:-cnt]
        return self.result_type(add_0x(bytes))

    def next_uint8(self, side: str = Side.Front) -> Any:
        return self.next_byte(side)

    def next_uint16(self, side: str = Side.Front) -> Any:
        return self.next_bytes(2, side)

    def next_uint24(self, side: str = Side.Front) -> Any:
        return self.next_bytes(3, side)

    def next_uint32(self, side: str = Side.Front) -> Any:
        return self.next_bytes(4, side)

    def next_uint128(self, side: str = Side.Front) -> Any:
        return self.next_bytes(16, side)

    def next_uint160(self, side: str = Side.Front) -> Any:
        return self.next_bytes(20, side)

    def next_uint256(self, side: str = Side.Front) -> Any:
        return self.next_bytes(32, side)
